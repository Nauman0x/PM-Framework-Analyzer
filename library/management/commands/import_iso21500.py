from django.core.management.base import BaseCommand
from library.models import Book, Page, Section
import os
import pdfplumber
import re


class Command(BaseCommand):
    help = 'Import ISO 21500 with exact section hierarchy'

    def handle(self, *args, **options):
        fpath = r"d:\Proj Management\ISO 21500-2021_ Project, programme and portfolio management - Context and concepts.pdf"
        
        if not os.path.exists(fpath):
            self.stderr.write(f"File not found: {fpath}")
            return
        
        # Clear existing ISO 21500 data
        book, created = Book.objects.get_or_create(
            title="ISO 21500-2021_ Project, programme and portfolio management - Context and concepts",
            defaults={'file_path': fpath}
        )
        book.sections.all().delete()
        book.pages.all().delete()
        
        self.stdout.write(f"Processing: {book.title}")
        
        # Define exact section hierarchy from TOC
        # Format: (section_number, title, start_page, level)
        # NOTE: These are TOC page numbers (printed page numbers in the document)
        sections_data = [
            ('', 'Introduction', 0, 1),  # Introduction page (no page number in TOC)
            ('1', 'Scope', 1, 1),
            ('2', 'Normative references', 1, 1),
            ('3', 'Terms and definitions', 1, 1),
            ('4', 'Project, programme and portfolio management concepts', 3, 1),
            ('4.1', 'General', 3, 2),
            ('4.2', 'Projects, programmes and portfolios', 4, 2),
            ('4.3', 'Organizational environment', 5, 2),
            ('4.4', 'External environment', 5, 2),
            ('4.5', 'Strategy implementation', 6, 2),
            ('4.6', 'Integrated governance and management approaches', 7, 2),
            ('5', 'Standards on project, programme and portfolio management', 8, 1),
            ('5.1', 'General', 8, 2),
            ('5.2', 'Overview', 9, 2),
            ('5.2.1', 'Core standards', 9, 3),
            ('5.2.2', 'Supporting standards and vocabulary', 9, 3),
            ('5.3', 'Benefits of using standards on project, programme and portfolio management', 10, 2),
            ('5.3.1', 'General', 10, 3),
            ('5.3.2', 'Project management', 10, 3),
            ('5.3.3', 'Programme management', 10, 3),
            ('5.3.4', 'Portfolio management', 10, 3),
            ('5.3.5', 'Governance', 11, 3),
            ('5.4', 'Organizational considerations for selection', 11, 2),
        ]
        
        try:
            with pdfplumber.open(fpath) as pdf:
                total_pages = len(pdf.pages)
                self.stdout.write(f"Total pages in PDF: {total_pages}")
                
                # Create sections with proper end pages
                # Note: Content ends at page 11 per TOC
                MAX_CONTENT_PAGE = 11
                created_sections = []
                for idx, (secnum, title, start, level) in enumerate(sections_data):
                    # Find next section with a DIFFERENT start page
                    end = MAX_CONTENT_PAGE
                    for next_idx in range(idx + 1, len(sections_data)):
                        next_start = sections_data[next_idx][2]
                        if next_start > start:
                            end = next_start - 1
                            break
                    
                    sec = Section.objects.create(
                        book=book,
                        title=title,
                        section_number=secnum,
                        level=level,
                        start_page=start,
                        end_page=end
                    )
                    created_sections.append(sec)
                    self.stdout.write(f"Created: {level} | {secnum:6} | {title[:40]:40} | Pages {start}-{end}")
                
                # Extract pages and section-specific content
                # NOTE: Section start/end pages are TOC page numbers (printed pages in document)
                # PDF page numbers = TOC page numbers + 6
                PAGE_OFFSET = 6
                
                all_pages_content = {}
                for i, page in enumerate(pdf.pages, start=1):
                    try:
                        raw = page.extract_text() or ''
                    except Exception:
                        raw = ''
                    
                    # Better text cleaning: preserve paragraphs
                    lines = raw.split('\n')
                    cleaned_lines = []
                    for line in lines:
                        cleaned = re.sub(r'[ \t]+', ' ', line).strip()
                        if cleaned:
                            cleaned_lines.append(cleaned)
                    all_pages_content[i] = '\n'.join(cleaned_lines)
                
                # Extract section-specific content by finding section markers
                for sec in created_sections:
                    section_content_parts = []
                    
                    # Convert TOC page numbers to actual PDF page numbers
                    pdf_start = sec.start_page + PAGE_OFFSET
                    pdf_end = sec.end_page + PAGE_OFFSET
                    
                    for page_num in range(pdf_start, pdf_end + 1):
                        if page_num not in all_pages_content:
                            continue
                        
                        page_text = all_pages_content[page_num]
                        
                        # Build section marker pattern
                        if sec.section_number:
                            marker_pattern = f"{re.escape(sec.section_number)}\\s+{re.escape(sec.title[:40])}"
                        else:
                            marker_pattern = re.escape(sec.title[:40])
                        
                        # Find where this section starts
                        match = re.search(marker_pattern, page_text, re.IGNORECASE)
                        if match:
                            start_pos = match.start()
                            
                            # Find where next section might start on same page
                            # Look for next numbered section pattern
                            remaining_text = page_text[start_pos:]
                            # Pattern for any section number followed by title
                            next_section_pattern = r'\n(\d+(?:\.\d+)*)\s+[A-Z]'
                            next_match = re.search(next_section_pattern, remaining_text[50:])  # Skip first 50 chars to avoid self-match
                            
                            if next_match:
                                section_text = remaining_text[:50 + next_match.start()]
                            else:
                                section_text = remaining_text
                            
                            section_content_parts.append(section_text.strip())
                        else:
                            # If marker not found and this is the only section on this page, use full page
                            # Check using PDF page numbers
                            sections_on_page = [s for s in created_sections 
                                              if (s.start_page + PAGE_OFFSET) <= page_num <= (s.end_page + PAGE_OFFSET)]
                            if len(sections_on_page) == 1:
                                section_content_parts.append(page_text)
                    
                    # Save extracted content to section
                    sec.content = '\n\n'.join(section_content_parts)
                    sec.save()
                
                # Create one Page object per page number for browsing
                for i in range(1, total_pages + 1):
                    if i in all_pages_content:
                        # Find primary section for this page (first one)
                        # Convert PDF page to TOC page for section lookup
                        toc_page = i - PAGE_OFFSET
                        assigned = None
                        for sec in created_sections:
                            if sec.start_page <= toc_page <= sec.end_page:
                                assigned = sec
                                break
                        
                        Page.objects.create(
                            book=book,
                            page_number=i,
                            text=all_pages_content[i],
                            section=assigned,
                            topic=(assigned.title if assigned else '')[:256]
                        )
                
                self.stdout.write(self.style.SUCCESS(
                    f"\nSuccessfully imported {total_pages} pages and {len(created_sections)} sections"
                ))
                
        except Exception as e:
            self.stderr.write(f"Error processing PDF: {e}")
            import traceback
            traceback.print_exc()
