from django.core.management.base import BaseCommand
from library.models import Book, Page, Section
import os
import pdfplumber
import re


class Command(BaseCommand):
    help = 'Import ISO 21502 with exact section hierarchy'

    def handle(self, *args, **options):
        fpath = r"d:\Proj Management\ISO 21502-2020_ Project, programme and portfolio management - Guidance on project management.pdf"
        
        if not os.path.exists(fpath):
            self.stderr.write(f"File not found: {fpath}")
            return
        
        # Clear existing ISO 21502 data
        book, created = Book.objects.get_or_create(
            title="ISO 21502-2020_ Project, programme and portfolio management - Guidance on project management",
            defaults={'file_path': fpath}
        )
        book.sections.all().delete()
        book.pages.all().delete()
        
        self.stdout.write(f"Processing: {book.title}")
        
        # Define exact section hierarchy from TOC - EXACT page numbers from user's TOC
        # Format: (section_number, title, start_page, level)
        sections_data = [
            ('1', 'Scope', 1, 1),
            ('2', 'Normative references', 1, 1),
            ('3', 'Terms and definitions', 1, 1),
            ('4', 'Project management concepts', 4, 1),
            ('4.1', 'Overview', 4, 2),
            ('4.1.1', 'General', 4, 3),
            ('4.1.2', 'Projects', 5, 3),
            ('4.1.3', 'Project management', 6, 3),
            ('4.2', 'Context', 6, 2),
            ('4.2.1', 'Impact of a project\'s context', 6, 3),
            ('4.2.2', 'Organizational strategy and projects', 6, 3),
            ('4.2.3', 'Customer and supplier perspective', 7, 3),
            ('4.2.4', 'Project constraints', 8, 3),
            ('4.2.5', 'Projects as stand-alone, part of a programme or part of a portfolio', 8, 3),
            ('4.3', 'Project governance', 9, 2),
            ('4.3.1', 'Governance framework', 9, 3),
            ('4.3.2', 'Business case', 9, 3),
            ('4.4', 'Project life cycle', 9, 2),
            ('4.5', 'Project organization and roles', 10, 2),
            ('4.5.1', 'Project organization', 10, 3),
            ('4.5.2', 'Sponsoring organization', 12, 3),
            ('4.5.3', 'Project board', 12, 3),
            ('4.5.4', 'Project sponsor', 12, 3),
            ('4.5.5', 'Project assurance', 13, 3),
            ('4.5.6', 'Project manager', 13, 3),
            ('4.5.7', 'Project office', 14, 3),
            ('4.5.8', 'Work package leader', 14, 3),
            ('4.5.9', 'Project team members', 14, 3),
            ('4.5.10', 'Project stakeholders', 15, 3),
            ('4.5.11', 'Other roles', 15, 3),
            ('4.6', 'Competencies of project personnel', 15, 2),
            ('5', 'Prerequisites for formalizing project management', 16, 1),
            ('5.1', 'Overview', 16, 2),
            ('5.2', 'Considerations for implementing project management', 16, 2),
            ('5.3', 'Continuous improvement of the project management environment', 16, 2),
            ('5.4', 'Alignment with organizational processes and systems', 17, 2),
            ('6', 'Integrated project management practices', 18, 1),
            ('6.1', 'Overview', 18, 2),
            ('6.2', 'Pre-project activities', 19, 2),
            ('6.3', 'Overseeing a project', 20, 2),
            ('6.4', 'Directing a project', 20, 2),
            ('6.5', 'Initiating a project', 21, 2),
            ('6.5.1', 'Overview', 21, 3),
            ('6.5.2', 'Project team mobilization', 21, 3),
            ('6.5.3', 'Project governance and management approach', 21, 3),
            ('6.5.4', 'Initial project justification', 21, 3),
            ('6.5.5', 'Initial project planning', 22, 3),
            ('6.6', 'Controlling a project', 22, 2),
            ('6.6.1', 'Overview', 22, 3),
            ('6.6.2', 'Progressive justification', 22, 3),
            ('6.6.3', 'Managing project performance', 22, 3),
            ('6.6.4', 'Managing the start and close of each project phase', 23, 3),
            ('6.6.5', 'Managing the start, progress and close of each work package', 24, 3),
            ('6.7', 'Managing delivery', 24, 2),
            ('6.8', 'Closing or terminating a project', 25, 2),
            ('6.9', 'Post-project activities', 26, 2),
            ('7', 'Management practices for a project', 26, 1),
            ('7.1', 'Overview', 26, 2),
            ('7.2', 'Planning', 27, 2),
            ('7.2.1', 'Overview', 27, 3),
            ('7.2.2', 'Developing the plan', 28, 3),
            ('7.2.3', 'Monitoring the plan', 28, 3),
            ('7.3', 'Benefit management', 28, 2),
            ('7.3.1', 'Overview', 28, 3),
            ('7.3.2', 'Identifying and analysing benefits', 28, 3),
            ('7.3.3', 'Monitoring benefits', 29, 3),
            ('7.3.4', 'Maintaining benefits', 29, 3),
            ('7.4', 'Scope management', 29, 2),
            ('7.4.1', 'Overview', 29, 3),
            ('7.4.2', 'Defining the scope', 30, 3),
            ('7.4.3', 'Controlling the scope', 30, 3),
            ('7.4.4', 'Confirming scope delivery', 30, 3),
            ('7.5', 'Resources management', 30, 2),
            ('7.5.1', 'Overview', 30, 3),
            ('7.5.2', 'Planning the project organization', 31, 3),
            ('7.5.3', 'Establishing the team', 31, 3),
            ('7.5.4', 'Developing the team', 31, 3),
            ('7.5.5', 'Managing the team', 31, 3),
            ('7.5.6', 'Planning, managing and controlling physical and material resources', 32, 3),
            ('7.6', 'Schedule management', 32, 2),
            ('7.6.1', 'Overview', 32, 3),
            ('7.6.2', 'Estimating activity durations', 32, 3),
            ('7.6.3', 'Developing the schedule', 33, 3),
            ('7.6.4', 'Controlling the schedule', 33, 3),
            ('7.7', 'Cost management', 33, 2),
            ('7.7.1', 'Overview', 33, 3),
            ('7.7.2', 'Estimating cost', 34, 3),
            ('7.7.3', 'Developing the budget', 34, 3),
            ('7.7.4', 'Controlling costs', 34, 3),
            ('7.8', 'Risk management', 34, 2),
            ('7.8.1', 'Overview', 34, 3),
            ('7.8.2', 'Identifying risk', 35, 3),
            ('7.8.3', 'Assessing risk', 35, 3),
            ('7.8.4', 'Treating risk', 35, 3),
            ('7.8.5', 'Controlling risk', 35, 3),
            ('7.9', 'Issues management', 35, 2),
            ('7.9.1', 'Overview', 35, 3),
            ('7.9.2', 'Identifying issues', 36, 3),
            ('7.9.3', 'Resolving issues', 36, 3),
            ('7.10', 'Change control', 36, 2),
            ('7.10.1', 'Overview', 36, 3),
            ('7.10.2', 'Establishing a change control framework', 37, 3),
            ('7.10.3', 'Identifying and assessing change requests', 37, 3),
            ('7.10.4', 'Planning the implementation of change requests', 37, 3),
            ('7.10.5', 'Implementing and closing change requests', 37, 3),
            ('7.11', 'Quality management', 37, 2),
            ('7.11.1', 'Overview', 37, 3),
            ('7.11.2', 'Planning quality', 38, 3),
            ('7.11.3', 'Assuring quality', 38, 3),
            ('7.11.4', 'Controlling quality', 38, 3),
            ('7.12', 'Stakeholder engagement', 39, 2),
            ('7.12.1', 'Overview', 39, 3),
            ('7.12.2', 'Identifying stakeholders', 39, 3),
            ('7.12.3', 'Engaging stakeholders', 40, 3),
            ('7.13', 'Communication management', 40, 2),
            ('7.13.1', 'Overview', 40, 3),
            ('7.13.2', 'Planning communication', 40, 3),
            ('7.13.3', 'Distributing information', 40, 3),
            ('7.13.4', 'Monitoring the impact of communications', 41, 3),
            ('7.14', 'Managing organizational and societal change', 41, 2),
            ('7.14.1', 'Overview', 41, 3),
            ('7.14.2', 'Identifying the need for change', 41, 3),
            ('7.14.3', 'Implementing the organizational and societal change', 42, 3),
            ('7.15', 'Reporting', 42, 2),
            ('7.15.1', 'Overview', 42, 3),
            ('7.15.2', 'Planning reporting', 42, 3),
            ('7.15.3', 'Managing reporting', 42, 3),
            ('7.15.4', 'Delivering reports', 42, 3),
            ('7.16', 'Information and documentation management', 43, 2),
            ('7.16.1', 'Overview', 43, 3),
            ('7.16.2', 'Identifying which information should be managed', 43, 3),
            ('7.16.3', 'Storing and retrieving information and documentation', 43, 3),
            ('7.17', 'Procurement', 43, 2),
            ('7.17.1', 'Overview', 43, 3),
            ('7.17.2', 'Planning procurement', 43, 3),
            ('7.17.3', 'Evaluating and selecting suppliers', 44, 3),
            ('7.17.4', 'Administering contracts', 44, 3),
            ('7.17.5', 'Closing contracts', 44, 3),
            ('7.18', 'Lessons learned', 44, 2),
            ('7.18.1', 'Overview', 44, 3),
            ('7.18.2', 'Identifying lessons', 45, 3),
            ('7.18.3', 'Disseminating lessons', 45, 3),
        ]
        
        try:
            with pdfplumber.open(fpath) as pdf:
                total_pages = len(pdf.pages)
                self.stdout.write(f"Total pages in PDF: {total_pages}")
                
                # Create sections with proper end pages
                # Note: Content ends at page 45 per TOC
                MAX_CONTENT_PAGE = 45
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
                    self.stdout.write(f"Created: L{level} | {secnum:8} | {title[:35]:35} | Pages {start}-{end}")
                
                # Extract pages and section-specific content
                # NOTE: Section start/end pages are TOC page numbers (printed pages in document)
                # PDF page numbers = TOC page numbers + 8
                PAGE_OFFSET = 8
                
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
                
                # Extract section-specific content by finding section number markers
                for sec in created_sections:
                    section_content_parts = []
                    
                    # Convert TOC page numbers to actual PDF page numbers
                    pdf_start = sec.start_page + PAGE_OFFSET
                    pdf_end = sec.end_page + PAGE_OFFSET
                    
                    for page_num in range(pdf_start, pdf_end + 1):
                        if page_num not in all_pages_content:
                            continue
                        
                        page_text = all_pages_content[page_num]
                        
                        # Find this section's starting position by looking for EXACT section number as standalone
                        start_pos = None
                        
                        if sec.section_number:
                            # Look for section number ONLY at start of line, followed by space and uppercase letter
                            # This ensures we match "4.2.3 Customer" but not "see 4.2.3" or "in 4.1.2 Projects"
                            pattern = f"^{re.escape(sec.section_number)}\\s+[A-Z]"
                            for match in re.finditer(pattern, page_text, re.MULTILINE):
                                start_pos = match.start()
                                break
                        else:
                            # For sections without numbers (like Introduction)
                            pattern = f"^{re.escape(sec.title[:30])}"
                            for match in re.finditer(pattern, page_text, re.MULTILINE | re.IGNORECASE):
                                start_pos = match.start()
                                break
                        
                        if start_pos is not None:
                            # Find where the next section number starts on this page
                            end_pos = len(page_text)
                            
                            # Look for ANY section number that comes after current position
                            # Pattern: start of line, then number.number format, then space
                            next_section_pattern = f"^(\\d+(?:\\.\\d+)*)\\s+[A-Z]"
                            
                            for next_match in re.finditer(next_section_pattern, page_text[start_pos + 10:], re.MULTILINE):
                                # Make sure this is a DIFFERENT section number
                                found_num = next_match.group(1)
                                if found_num != sec.section_number:
                                    end_pos = start_pos + 10 + next_match.start()
                                    break
                            
                            section_text = page_text[start_pos:end_pos].strip()
                            if section_text:
                                section_content_parts.append(section_text)
                        elif len([s for s in created_sections if s.start_page <= page_num <= s.end_page]) == 1:
                            # Only section on this page - use full page
                            section_content_parts.append(page_text)
                    
                    # Save extracted content
                    content = '\n\n'.join(section_content_parts)
                    if not content and sec.section_number:
                        # If no content found, mark as heading-only
                        content = f"{sec.section_number} {sec.title}"
                    sec.content = content
                    sec.save()
                
                # Create one Page object per page number for browsing
                for i in range(1, total_pages + 1):
                    if i in all_pages_content:
                        # Find primary section for this page (first one)
                        assigned = None
                        for sec in created_sections:
                            if sec.start_page <= i <= sec.end_page:
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
