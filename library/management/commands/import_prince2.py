from django.core.management.base import BaseCommand
from library.models import Book, Page, Section
import os
import pdfplumber
import re


class Command(BaseCommand):
    help = 'Import PRINCE2 with exact section hierarchy'

    def handle(self, *args, **options):
        fpath = r"d:\Proj Management\Managing Successful Projects with PRINCE2® -- Andy Murray -- 7, 2023 -- PeopleCert International Limited.pdf"
        
        if not os.path.exists(fpath):
            self.stderr.write(f"File not found: {fpath}")
            return
        
        # Clear existing PRINCE2 data
        book, created = Book.objects.get_or_create(
            title="Managing Successful Projects with PRINCE2",
            defaults={'file_path': fpath}
        )
        book.sections.all().delete()
        book.pages.all().delete()
        
        self.stdout.write(f"Processing: {book.title}")
        
        # Define exact section hierarchy from TOC
        # Format: (section_number, title, start_page, level)
        # NOTE: These are TOC page numbers (printed page numbers in the document)
        sections_data = [
            ('1', 'Introduction', 1, 1),
            ('1.1', 'Introduction', 2, 2),
            ('1.1.1', 'Purpose of this book', 2, 3),
            ('1.2', 'Structure of the official book', 3, 2),
            ('1.3', 'What is a project?', 5, 2),
            ('1.4', 'What is project management?', 6, 2),
            ('1.5', 'The project context', 7, 2),
            ('1.5.1', 'Organizational context', 8, 3),
            ('1.5.2', 'Commercial context', 9, 3),
            ('1.5.3', 'Delivery method', 10, 3),
            ('1.5.4', 'Sustainability context', 10, 3),
            ('1.5.5', 'Scale', 11, 3),
            ('1.6', 'Features and benefits of PRINCE2', 12, 2),
            ('1.7', 'Example scenarios', 12, 2),
            ('2', 'Principles', 19, 1),
            ('2.1', 'Ensure continued business justification', 21, 2),
            ('2.2', 'Learn from experience', 22, 2),
            ('2.3', 'Define roles, responsibilities, and relationships', 24, 2),
            ('2.4', 'Manage by exception', 25, 2),
            ('2.5', 'Manage by stages', 27, 2),
            ('2.6', 'Focus on products', 28, 2),
            ('2.7', 'Tailor to suit the project', 29, 2),
            ('3', 'People', 31, 1),
            ('3.1', 'Context', 32, 2),
            ('3.2', 'Leading successful change', 34, 2),
            ('3.2.1', 'Projects require change management', 34, 3),
            ('3.2.2', 'Stakeholders', 36, 3),
            ('3.2.3', 'Culture', 37, 3),
            ('3.3', 'Leading successful teams', 39, 2),
            ('3.3.1', 'Leading across organizational boundaries', 40, 3),
            ('3.3.2', 'Building effective teams', 40, 3),
            ('3.3.3', 'Bringing the team together', 41, 3),
            ('3.4', 'Communication', 42, 2),
            ('3.5', 'People are central to the method', 45, 2),
            ('3.5.1', 'People and PRINCE2 principles', 46, 3),
            ('3.5.2', 'People and PRINCE2 practices', 47, 3),
            ('3.5.3', 'People and PRINCE2 processes', 48, 3),
            ('4', 'Introduction to PRINCE2 Practices', 49, 1),
            ('4.1', 'The PRINCE2 practices', 50, 2),
            ('4.2', 'Applying the practices', 51, 2),
            ('4.3', 'Management products', 52, 2),
            ('4.3.1', 'Project initiation documentation', 52, 3),
            ('4.3.2', 'Project log', 53, 3),
            ('4.4', 'Format of the practice chapters', 54, 2),
            ('5', 'Business case', 55, 1),
            ('5.1', 'Purpose', 56, 2),
            ('5.2', 'Guidance for effective business case management', 58, 2),
            ('5.2.1', 'Business case lifecycle', 58, 3),
            ('5.2.3', 'Establishing business justification', 60, 3),
            ('5.3', 'Techniques', 60, 2),
            ('5.3.1', 'PRINCE2 technique for business case management', 60, 3),
            ('5.3.2', 'Supporting techniques', 64, 3),
            ('5.4', 'Applying the practice', 65, 2),
            ('5.4.1', 'Organizational context', 65, 3),
            ('5.4.2', 'Commercial context', 66, 3),
            ('5.4.3', 'Delivery method', 66, 3),
            ('5.4.4', 'Sustainability', 66, 3),
            ('5.4.5', 'Scale', 67, 3),
            ('5.5', 'Management products to support the practice', 68, 2),
            ('5.6', 'Focus of key roles for the practice', 71, 2),
            ('5.7', 'Key relationships with principles', 72, 2),
            ('6', 'Organizing', 73, 1),
            ('6.1', 'Purpose', 74, 2),
            ('6.2', 'Guidance for effective organizing', 74, 2),
            ('6.2.1', 'The three project interests', 74, 3),
            ('6.2.2', 'Organizational levels', 76, 3),
            ('6.2.3', 'Project management team structure', 77, 3),
            ('6.2.4', 'PRINCE2 roles', 78, 3),
            ('6.2.5', 'Work breakdown structure', 83, 3),
            ('6.3', 'Techniques', 83, 2),
            ('6.3.2', 'Supporting techniques', 86, 3),
            ('6.4', 'Applying the practice', 88, 2),
            ('6.4.1', 'Organizational context', 88, 3),
            ('6.4.2', 'Commercial context', 89, 3),
            ('6.4.3', 'Delivery method', 90, 3),
            ('6.4.4', 'Sustainability', 91, 3),
            ('6.4.5', 'Scale', 91, 3),
            ('6.5', 'Management products to support the practice', 92, 2),
            ('6.6', 'Focus of key roles for the practice', 93, 2),
            ('6.7', 'Key relationships with principles', 95, 2),
            ('7', 'Plans', 97, 1),
            ('7.1', 'Purpose', 98, 2),
            ('7.1.1', 'Plans enable understanding and communication', 98, 3),
            ('7.1.2', 'Plans enable control', 99, 3),
            ('7.2', 'Guidance for effective planning', 99, 2),
            ('7.2.1', 'Planning horizon', 99, 3),
            ('7.2.2', 'Levels of plans', 101, 3),
            ('7.2.3', 'Stages', 103, 3),
            ('7.2.4', 'Tolerances in planning', 105, 3),
            ('7.2.5', 'Product-based planning', 107, 3),
            ('7.3', 'Techniques', 107, 2),
            ('7.3.1', 'PRINCE2 technique for planning', 107, 3),
            ('7.3.2', 'Defining and analysing the products', 108, 3),
            ('7.3.3', 'Supporting techniques', 116, 3),
            ('7.3.4', 'Estimating', 117, 3),
            ('7.4', 'Applying the practice', 118, 2),
            ('7.4.1', 'Organizational context', 118, 3),
            ('7.4.2', 'Commercial context', 118, 3),
            ('7.4.3', 'Delivery method', 119, 3),
            ('7.4.4', 'Sustainability', 120, 3),
            ('7.4.5', 'Scale', 120, 3),
            ('7.5', 'Management products to support the practice', 121, 2),
            ('7.6', 'Focus of key roles for the practice', 124, 2),
            ('7.7', 'Key relationships with principles', 125, 2),
            ('8', 'Quality', 127, 1),
            ('8.1', 'Purpose', 128, 2),
            ('8.1.1', 'Key quality terminology', 129, 3),
            ('8.1.2', 'Product-based quality', 130, 3),
            ('8.2', 'Guidance for effective quality management', 130, 2),
            ('8.2.1', 'Quality planning', 131, 3),
            ('8.2.2', 'Quality control', 133, 3),
            ('8.2.3', 'Quality assurance', 135, 3),
            ('8.3', 'Techniques', 135, 2),
            ('8.3.1', 'PRINCE2 techniques for quality management', 135, 3),
            ('8.3.2', 'Supporting techniques', 139, 3),
            ('8.4', 'Applying the practice', 140, 2),
            ('8.4.1', 'Organizational context', 140, 3),
            ('8.4.2', 'Commercial context', 140, 3),
            ('8.4.3', 'Delivery method', 141, 3),
            ('8.4.4', 'Sustainability', 142, 3),
            ('8.4.5', 'Scale', 142, 3),
            ('8.5', 'Management products to support the practice', 143, 2),
            ('8.6', 'Focus of key roles for the practice', 145, 2),
            ('8.7', 'Key relationships with principles', 146, 2),
            ('9', 'Risk', 147, 1),
            ('9.1', 'Purpose', 148, 2),
            ('9.2', 'Guidance for effective risk management', 149, 2),
            ('9.2.1', 'Risk planning', 150, 3),
            ('9.2.2', 'Risk analysis', 150, 3),
            ('9.2.3', 'Risk control', 151, 3),
            ('9.2.4', 'Risk culture', 154, 3),
            ('9.3', 'Techniques', 155, 2),
            ('9.3.1', 'PRINCE2 technique for risk management', 155, 3),
            ('9.3.2', 'Supporting techniques', 158, 3),
            ('9.4', 'Applying the practice', 160, 2),
            ('9.4.1', 'Organizational context', 160, 3),
            ('9.4.2', 'Commercial context', 161, 3),
            ('9.4.3', 'Delivery method', 161, 3),
            ('9.4.4', 'Sustainability', 161, 3),
            ('9.4.5', 'Scale', 162, 3),
            ('9.5', 'Management products to support the practice', 162, 2),
            ('9.6', 'Focus of key roles for the practice', 164, 2),
            ('9.7', 'Key relationships with principles', 165, 2),
            ('10', 'Issues', 167, 1),
            ('10.1', 'Purpose', 168, 2),
            ('10.2', 'Guidance for effective issue management', 169, 2),
            ('10.2.1', 'Baselines', 169, 3),
            ('10.2.2', 'Issue resolution', 170, 3),
            ('10.2.3', 'Change control', 172, 3),
            ('10.2.4', 'Delegating authority for changes', 173, 3),
            ('10.2.5', 'Change budget', 173, 3),
            ('10.3', 'Techniques', 173, 2),
            ('10.3.1', 'PRINCE2 Technique for issue management', 173, 3),
            ('10.3.2', 'Supporting techniques', 177, 3),
            ('10.4', 'Applying the practice', 177, 2),
            ('10.4.1', 'Organizational context', 177, 3),
            ('10.4.2', 'Commercial context', 177, 3),
            ('10.4.3', 'Delivery method', 178, 3),
            ('10.4.4', 'Sustainability', 179, 3),
            ('10.4.5', 'Scale', 179, 3),
            ('10.5', 'Management products to support the practice', 180, 2),
            ('10.6', 'Focus of key roles for the practice', 182, 2),
            ('10.7', 'Key relationships with principles', 183, 2),
            ('11', 'Progress', 185, 1),
            ('11.1', 'Purpose', 186, 2),
            ('11.2', 'Guidance for effective progress management', 187, 2),
            ('11.2.2', 'Types of control', 190, 3),
            ('11.2.3', 'Reviewing progress and lessons', 190, 3),
            ('11.2.4', 'Reporting progress and lessons', 192, 3),
            ('11.2.5', 'Forecasting', 193, 3),
            ('11.2.6', 'Escalating', 194, 3),
            ('11.2.7', 'Use of data and systems in progress management', 195, 3),
            ('11.3', 'Techniques: progress management', 196, 2),
            ('11.3.1', 'PRINCE2 technique for exception management', 196, 3),
            ('11.3.2', 'Supporting techniques', 198, 3),
            ('11.4', 'Applying the progress practice', 202, 2),
            ('11.4.1', 'Organizational context', 202, 3),
            ('11.4.2', 'Commercial context', 202, 3),
            ('11.4.3', 'Delivery method', 202, 3),
            ('11.4.4', 'Sustainability', 203, 3),
            ('11.4.5', 'Scale', 203, 3),
            ('11.5', 'Management products to support the practice', 204, 2),
            ('11.6', 'Focus of key roles for the practice', 209, 2),
            ('11.7', 'Key relationships with principles', 211, 2),
            ('12', 'Introduction to PRINCE2 Processes', 213, 1),
            ('12.1', 'The PRINCE2 journey', 215, 2),
            ('12.1.1', 'Pre-project', 215, 3),
            ('12.1.2', 'Initiation stage', 215, 3),
            ('12.1.3', 'Subsequent stages', 215, 3),
            ('12.1.4', 'Final stage', 216, 3),
            ('12.1.5', 'Post-project', 216, 3),
            ('12.2', 'The PRINCE2 process model', 216, 2),
            ('12.3', 'Format of the process chapters', 218, 2),
            ('13', 'Starting up a project', 219, 1),
            ('13.1', 'Purpose', 220, 2),
            ('13.2', 'Objectives', 220, 2),
            ('13.3', 'Context', 221, 2),
            ('13.4', 'Activities', 222, 2),
            ('13.4.2', 'Assess previous lessons', 223, 3),
            ('13.4.3', 'Prepare the outline business case', 223, 3),
            ('13.4.4', 'Appoint the project management team', 223, 3),
            ('13.4.5', 'Select the project approach', 224, 3),
            ('13.4.6', 'Assemble the project brief', 224, 3),
            ('13.4.7', 'Plan the initiation stage', 225, 3),
            ('13.4.8', 'Request project initiation', 225, 3),
            ('13.5', 'Applying the process', 225, 2),
            ('13.5.1', 'General considerations', 225, 3),
            ('13.5.2', 'Tailoring roles in starting up a project', 226, 3),
            ('13.6', 'Responsibilities', 226, 2),
            ('13.7', 'Application of the practices to this process', 227, 2),
            ('14', 'Directing a project', 229, 1),
            ('14.1', 'Purpose', 230, 2),
            ('14.2', 'Objectives', 230, 2),
            ('14.3', 'Context', 230, 2),
            ('14.4', 'Activities', 232, 2),
            ('14.4.1', 'Authorize initiation', 232, 3),
            ('14.4.2', 'Authorize the project', 233, 3),
            ('14.4.3', 'Give ongoing direction', 234, 3),
            ('14.4.4', 'Authorize a stage or exception plan', 235, 3),
            ('14.4.5', 'Authorize project closure', 235, 3),
            ('14.5', 'Applying the process', 236, 2),
            ('14.6', 'Responsibilities', 236, 2),
            ('14.7', 'Application of the practices to this process', 237, 2),
            ('15', 'Initiating a project', 239, 1),
            ('15.1', 'Purpose', 240, 2),
            ('15.2', 'Objectives', 240, 2),
            ('15.3', 'Context', 241, 2),
            ('15.4', 'Activities', 242, 2),
            ('15.4.1', 'Agree tailoring requirements', 242, 3),
            ('15.4.2', 'Agree the management approaches', 243, 3),
            ('15.4.3', 'Establish project controls', 243, 3),
            ('15.4.4', 'Prepare the project plan', 245, 3),
            ('15.4.5', 'Prepare the full business case', 246, 3),
            ('15.4.6', 'Assemble the project initiation documentation', 246, 3),
            ('15.4.7', 'Request project authorization', 247, 3),
            ('15.5', 'Applying the process', 247, 2),
            ('15.5.1', 'General considerations', 247, 3),
            ('15.5.2', 'Tailoring roles in initiating a project', 248, 3),
            ('15.6', 'Responsibilities', 248, 2),
            ('15.7', 'Application of the practices to this process', 249, 2),
            ('16', 'Controlling a stage', 251, 1),
            ('16.1', 'Purpose', 252, 2),
            ('16.2', 'Objectives', 252, 2),
            ('16.3', 'Context', 253, 2),
            ('16.4', 'Activities', 254, 2),
            ('16.4.1', 'Authorize a work package', 254, 3),
            ('16.4.2', 'Evaluate work package status', 255, 3),
            ('16.4.3', 'Receive completed work package', 256, 3),
            ('16.4.4', 'Evaluate stage status', 256, 3),
            ('16.4.5', 'Capture issues and risks', 256, 3),
            ('16.4.6', 'Take corrective action', 257, 3),
            ('16.4.7', 'Escalate issues and risks', 257, 3),
            ('16.4.8', 'Report highlights', 258, 3),
            ('16.5', 'Applying the process', 259, 2),
            ('16.5.1', 'General considerations', 259, 3),
            ('16.5.2', 'Tailoring roles in controlling a stage', 259, 3),
            ('16.6', 'Responsibilities', 259, 2),
            ('16.7', 'Application of the practices to this process', 260, 2),
            ('17', 'Managing product delivery', 261, 1),
            ('17.1', 'Purpose', 262, 2),
            ('17.2', 'Objectives', 262, 2),
            ('17.3', 'Context', 263, 2),
            ('17.4', 'Activities', 264, 2),
            ('17.4.1', 'Accept a work package', 264, 3),
            ('17.4.2', 'Execute a work package', 265, 3),
            ('17.4.3', 'Evaluate a work package', 265, 3),
            ('17.4.4', 'Notify work package completion', 265, 3),
            ('17.5', 'Applying the process', 266, 2),
            ('17.5.1', 'General considerations', 266, 3),
            ('17.5.2', 'Tailoring roles in managing product delivery', 266, 3),
            ('17.6', 'Responsibilities', 267, 2),
            ('17.7', 'Application of the practices to this process', 267, 2),
            ('18', 'Managing a stage boundary', 269, 1),
            ('18.1', 'Purpose', 270, 2),
            ('18.2', 'Objectives', 270, 2),
            ('18.3', 'Context', 271, 2),
            ('18.4', 'Activities', 272, 2),
            ('18.4.1', 'Prepare the next stage plan', 272, 3),
            ('18.4.2', 'Prepare the exception plan (if required)', 273, 3),
            ('18.4.3', 'Update the project plan', 273, 3),
            ('18.4.4', 'Update the business case', 274, 3),
            ('18.4.5', 'Evaluate the stage', 274, 3),
            ('18.4.6', 'Request the next stage', 275, 3),
            ('18.5', 'Applying the process', 275, 2),
            ('18.5.1', 'General considerations', 275, 3),
            ('18.6', 'Responsibilities', 275, 2),
            ('18.7', 'Application of the practices to this process', 276, 2),
            ('19', 'Closing a project', 277, 1),
            ('19.1', 'Purpose', 278, 2),
            ('19.2', 'Objectives', 278, 2),
            ('19.3', 'Context', 279, 2),
            ('19.4', 'Activities', 280, 2),
            ('19.4.1', 'Prepare planned closure', 280, 3),
            ('19.4.2', 'Prepare premature closure', 281, 3),
            ('19.4.3', 'Confirm project acceptance', 281, 3),
            ('19.4.4', 'Evaluate the project', 282, 3),
            ('19.4.5', 'Request project closure', 282, 3),
            ('19.5', 'Applying the process', 283, 2),
            ('19.5.1', 'General considerations', 283, 3),
            ('19.5.2', 'Tailoring roles in closing a project', 283, 3),
            ('19.6', 'Responsibilities', 283, 2),
            ('19.7', 'Application of the practices to this process', 283, 2),
        ]
        
        try:
            with pdfplumber.open(fpath) as pdf:
                total_pages = len(pdf.pages)
                self.stdout.write(f"Total pages in PDF: {total_pages}")
                
                # Create sections with proper end pages
                # Note: Content ends at page 283 per TOC
                MAX_CONTENT_PAGE = 283
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
                # PDF page numbers = TOC page numbers + 19
                PAGE_OFFSET = 19
                
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
                            # This ensures we match "1 Introduction" but not "see 1.2" or "in 1.3 What"
                            pattern = f"^{re.escape(sec.section_number)}\\s+[A-Z]"
                            for match in re.finditer(pattern, page_text, re.MULTILINE):
                                start_pos = match.start()
                                break
                        else:
                            # For sections without numbers
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
                        else:
                            # Check using PDF page numbers - if this is the only section on this page, use full page
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
