from django.core.management.base import BaseCommand
from library.models import Book, Page
import os
import pdfplumber
from library.models import Section
import re


class Command(BaseCommand):
    help = 'Import PDFs from a directory, storing pages and text.'

    def add_arguments(self, parser):
        parser.add_argument('dir', help='Directory containing PDF files to import')

    def handle(self, *args, **options):
        dirpath = options['dir']
        if not os.path.isdir(dirpath):
            self.stderr.write(f"Not a directory: {dirpath}")
            return

        for fname in os.listdir(dirpath):
            if not fname.lower().endswith('.pdf'):
                continue
            fpath = os.path.join(dirpath, fname)
            title = os.path.splitext(fname)[0]
            book, created = Book.objects.get_or_create(title=title, file_path=fpath)
            if created:
                self.stdout.write(f"Created book: {title}")
            else:
                self.stdout.write(f"Updating book: {title}")
                # Clear old sections and pages
                book.sections.all().delete()
                book.pages.all().delete()

            # extract pages
            try:
                with pdfplumber.open(fpath) as pdf:
                    total_pages = len(pdf.pages)
                    # attempt to get outline / table of contents
                    outlines = []
                    try:
                        outlines = pdf.outlines or []
                    except Exception:
                        outlines = []

                    sections = []
                    if outlines:
                        # pdfplumber outlines are nested; flatten with page numbers
                        def flatten(outlist, level=1):
                            res = []
                            for item in outlist:
                                if isinstance(item, dict) and 'title' in item:
                                    sec_title = item.get('title', '').strip()
                                    try:
                                        pnum = item.get('page_number') or item.get('page') or None
                                        if pnum is not None:
                                            pnum = int(pnum)
                                    except Exception:
                                        pnum = None
                                    
                                    # Extract section number from title
                                    secnum = None
                                    if pnum:
                                        # Try to extract numbering like "1", "1.1", "4.2.3" from title
                                        num_match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+)$', sec_title)
                                        if num_match:
                                            secnum = num_match.group(1)
                                            sec_title = num_match.group(2)
                                        res.append((sec_title, pnum, level, secnum))
                                    
                                    if item.get('children'):
                                        res.extend(flatten(item.get('children'), level+1))
                            return res

                        entries = flatten(outlines)
                        for sec_title, pnum, level, secnum in entries:
                            if pnum and 1 <= pnum <= total_pages:
                                sections.append({
                                    'title': sec_title, 
                                    'start_page': pnum, 
                                    'level': level,
                                    'section_number': secnum or ''
                                })

                    # fallback: text-based heading detection with section numbering
                    if not sections:
                        for i, page in enumerate(pdf.pages, start=1):
                            try:
                                text = page.extract_text() or ''
                            except Exception:
                                text = ''
                            
                            # Split into lines and check for section headings
                            lines = [l.strip() for l in text.splitlines() if l.strip()]
                            
                            for ln in lines[:20]:  # Check first 20 lines
                                # Pattern for numbered sections: "1 Scope", "4.2 Projects, programmes...", "5.2.1 Core standards"
                                num_match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+)$', ln)
                                if num_match and len(ln) < 200:
                                    secnum = num_match.group(1)
                                    sec_title = num_match.group(2).strip()
                                    level = secnum.count('.') + 1
                                    
                                    # Skip if it looks like a page number or figure reference
                                    if sec_title.lower().startswith(('page ', 'figure ', 'table ', 'note ')):
                                        continue
                                    
                                    sections.append({
                                        'title': sec_title,
                                        'start_page': i,
                                        'level': level,
                                        'section_number': secnum
                                    })
                                    break
                                # Also detect non-numbered headings (like "Introduction", "Foreword")
                                elif (ln.isupper() or (ln[0].isupper() and len(ln.split()) <= 5)) and len(ln) < 100 and len(ln) > 3:
                                    # Skip common non-heading uppercase text
                                    skip_words = ['ISO', 'INTERNATIONAL', 'STANDARD', 'COPYRIGHT', 'NOTE']
                                    if not any(ln.startswith(w) for w in skip_words):
                                        sections.append({
                                            'title': ln,
                                            'start_page': i,
                                            'level': 1,
                                            'section_number': ''
                                        })
                                        break

                    # ensure sections sorted by start_page
                    sections = sorted(sections, key=lambda s: s['start_page'])

                    # create sections with inferred end_page (next start -1)
                    created_sections = []
                    for idx, s in enumerate(sections):
                        start = s['start_page']
                        end = sections[idx+1]['start_page'] - 1 if idx + 1 < len(sections) else total_pages
                        sec = Section.objects.create(
                            book=book,
                            title=s.get('title')[:1024],
                            section_number=s.get('section_number', '')[:64],
                            level=s.get('level', 1),
                            start_page=start,
                            end_page=end
                        )
                        created_sections.append(sec)

                    # extract pages and attach to sections with better text formatting
                    for i, page in enumerate(pdf.pages, start=1):
                        try:
                            raw = page.extract_text() or ''
                        except Exception:
                            raw = ''
                        
                        # Better text cleaning: preserve paragraphs but normalize whitespace within lines
                        lines = raw.split('\n')
                        cleaned_lines = []
                        for line in lines:
                            cleaned = re.sub(r'[ \t]+', ' ', line).strip()
                            if cleaned:
                                cleaned_lines.append(cleaned)
                        text = '\n'.join(cleaned_lines)

                        # find section for this page
                        assigned = None
                        for sec in created_sections:
                            if sec.start_page <= i <= (sec.end_page or sec.start_page):
                                assigned = sec
                                break

                        p, pc = Page.objects.update_or_create(
                            book=book, page_number=i,
                            defaults={'text': text, 'section': assigned, 'topic': (assigned.title if assigned else '')[:256]}
                        )
                    self.stdout.write(f"Imported {total_pages} pages and {len(created_sections)} sections from {fname}")
            except Exception as e:
                self.stderr.write(f"Failed to process {fname}: {e}")
