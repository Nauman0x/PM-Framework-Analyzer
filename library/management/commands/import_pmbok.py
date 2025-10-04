import os
import pdfplumber
import re
from django.core.management.base import BaseCommand
from library.models import Book, Page, Section

class Command(BaseCommand):
    help = 'Import PMBOK Guide 7th Edition with both parts'

    def handle(self, *args, **options):
        pdf_filename = "Project-Management-Institute-A-Guide-to-the-Project-Management-Body-of-Knowledge-PMBOK-R-Guide-PMBOK®️-Guide-Project-Management-Institute-2021.pdf"
        pdf_path = os.path.join(r"d:\Proj Management", pdf_filename)
        
        # The PMBOK Guide has two main parts with separate page numbering
        # Part 1: THE STANDARD FOR PROJECT MANAGEMENT (pages 3-60, PDF pages 30-87)
        # Part 2: A GUIDE TO THE PMBOK (pages 3-232, PDF pages 98-327)
        
        STANDARD_OFFSET = 27  # THE STANDARD starts at PDF page 30 (TOC page 3)
        GUIDE_OFFSET = 95     # THE GUIDE starts at PDF page 98 (TOC page 3)
        
        MAX_PDF_PAGE = 370  # Total pages in PDF
        
        # Define sections based on TOC
        # Format: (section_number, title, toc_page, level, part)
        # part: 'STANDARD' or 'GUIDE'
        sections_data = [
            # THE STANDARD FOR PROJECT MANAGEMENT
            ('1', 'INTRODUCTION', 3, 1, 'STANDARD'),
            ('1.1', 'Purpose of The Standard for Project Management', 3, 2, 'STANDARD'),
            ('1.2', 'Key Terms and Concepts', 4, 2, 'STANDARD'),
            ('1.3', 'Audience for this Standard', 5, 2, 'STANDARD'),
            
            ('2', 'A SYSTEM FOR VALUE DELIVERY', 7, 1, 'STANDARD'),
            ('2.1', 'Creating Value', 7, 2, 'STANDARD'),
            ('2.1.1', 'Value Delivery Components', 8, 3, 'STANDARD'),
            ('2.1.2', 'Information Flow', 11, 3, 'STANDARD'),
            ('2.2', 'Organizational Governance Systems', 12, 2, 'STANDARD'),
            ('2.3', 'Functions Associated with Projects', 12, 2, 'STANDARD'),
            ('2.3.1', 'Provide Oversight and Coordination', 13, 3, 'STANDARD'),
            ('2.3.2', 'Present Objectives and Feedback', 13, 3, 'STANDARD'),
            ('2.3.3', 'Facilitate and Support', 14, 3, 'STANDARD'),
            ('2.3.4', 'Perform Work and Contribute Insights', 14, 3, 'STANDARD'),
            ('2.3.5', 'Apply Expertise', 15, 3, 'STANDARD'),
            ('2.3.6', 'Provide Business Direction and Insight', 15, 3, 'STANDARD'),
            ('2.3.7', 'Provide Resources and Direction', 15, 3, 'STANDARD'),
            ('2.3.8', 'Maintain Governance', 16, 3, 'STANDARD'),
            ('2.4', 'The Project Environment', 16, 2, 'STANDARD'),
            ('2.4.1', 'Internal Environment', 16, 3, 'STANDARD'),
            ('2.4.2', 'External Environment', 18, 3, 'STANDARD'),
            ('2.5', 'Product Management Considerations', 18, 2, 'STANDARD'),
            
            ('3', 'PROJECT MANAGEMENT PRINCIPLES', 21, 1, 'STANDARD'),
            ('3.1', 'Be a Diligent, Respectful, and Caring Steward', 24, 2, 'STANDARD'),
            ('3.2', 'Create a Collaborative Project Team Environment', 28, 2, 'STANDARD'),
            ('3.3', 'Effectively Engage with Stakeholders', 31, 2, 'STANDARD'),
            ('3.4', 'Focus on Value', 34, 2, 'STANDARD'),
            ('3.5', 'Recognize, Evaluate, and Respond to System Interactions', 37, 2, 'STANDARD'),
            ('3.6', 'Demonstrate Leadership Behaviors', 40, 2, 'STANDARD'),
            ('3.7', 'Tailor Based on Context', 44, 2, 'STANDARD'),
            ('3.8', 'Build Quality into Processes and Deliverables', 47, 2, 'STANDARD'),
            ('3.9', 'Navigate Complexity', 50, 2, 'STANDARD'),
            ('3.10', 'Optimize Risk Responses', 53, 2, 'STANDARD'),
            ('3.11', 'Embrace Adaptability and Resiliency', 55, 2, 'STANDARD'),
            ('3.12', 'Enable Change to Achieve the Envisioned Future State', 58, 2, 'STANDARD'),
            
            # A GUIDE TO THE PROJECT MANAGEMENT BODY OF KNOWLEDGE (PMBOK® GUIDE)
            ('1', 'INTRODUCTION', 3, 1, 'GUIDE'),
            ('1.1', 'Structure of the PMBOK® Guide', 3, 2, 'GUIDE'),
            ('1.2', 'Relationship of the PMBOK® Guide and The Standard for Project Management', 4, 2, 'GUIDE'),
            ('1.3', 'Changes to the PMBOK® Guide', 6, 2, 'GUIDE'),
            ('1.4', 'Relationship to PMIstandards+', 6, 2, 'GUIDE'),
            
            ('2', 'PROJECT PERFORMANCE DOMAINS', 7, 1, 'GUIDE'),
            ('2.1', 'Stakeholder Performance Domain', 8, 2, 'GUIDE'),
            ('2.1.1', 'Stakeholder Engagement', 10, 3, 'GUIDE'),
            ('2.1.2', 'Interactions with Other Performance Domains', 14, 3, 'GUIDE'),
            ('2.1.3', 'Checking Results', 15, 3, 'GUIDE'),
            
            ('2.2', 'Team Performance Domain', 16, 2, 'GUIDE'),
            ('2.2.1', 'Project Team Management and Leadership', 17, 3, 'GUIDE'),
            ('2.2.2', 'Project Team Culture', 20, 3, 'GUIDE'),
            ('2.2.3', 'High-Performing Project Teams', 22, 3, 'GUIDE'),
            ('2.2.4', 'Leadership Skills', 23, 3, 'GUIDE'),
            ('2.2.5', 'Tailoring Leadership Styles', 30, 3, 'GUIDE'),
            ('2.2.6', 'Interactions with Other Performance Domains', 31, 3, 'GUIDE'),
            ('2.2.7', 'Checking Results', 31, 3, 'GUIDE'),
            
            ('2.3', 'Development Approach and Life Cycle Performance Domain', 32, 2, 'GUIDE'),
            ('2.3.1', 'Development, Cadence, and Life Cycle Relationship', 33, 3, 'GUIDE'),
            ('2.3.2', 'Delivery Cadence', 33, 3, 'GUIDE'),
            ('2.3.3', 'Development Approaches', 35, 3, 'GUIDE'),
            ('2.3.4', 'Considerations for Selecting a Development Approach', 39, 3, 'GUIDE'),
            ('2.3.5', 'Life Cycle and Phase Definitions', 42, 3, 'GUIDE'),
            ('2.3.6', 'Aligning of Delivery Cadence, Development Approach, and Life Cycle', 46, 3, 'GUIDE'),
            ('2.3.7', 'Interactions with Other Performance Domains', 49, 3, 'GUIDE'),
            ('2.3.8', 'Measuring Outcomes', 50, 3, 'GUIDE'),
            
            ('2.4', 'Planning Performance Domain', 51, 2, 'GUIDE'),
            ('2.4.1', 'Planning Overview', 52, 3, 'GUIDE'),
            ('2.4.2', 'Planning Variables', 53, 3, 'GUIDE'),
            ('2.4.3', 'Project Team Composition and Structure', 63, 3, 'GUIDE'),
            ('2.4.4', 'Communication', 64, 3, 'GUIDE'),
            ('2.4.5', 'Physical Resources', 65, 3, 'GUIDE'),
            ('2.4.6', 'Procurement', 65, 3, 'GUIDE'),
            ('2.4.7', 'Changes', 66, 3, 'GUIDE'),
            ('2.4.8', 'Metrics', 66, 3, 'GUIDE'),
            ('2.4.9', 'Alignment', 67, 3, 'GUIDE'),
            ('2.4.10', 'Interactions with Other Performance Domains', 67, 3, 'GUIDE'),
            ('2.4.11', 'Checking Results', 68, 3, 'GUIDE'),
            
            ('2.5', 'Project Work Performance Domain', 69, 2, 'GUIDE'),
            ('2.5.1', 'Project Processes', 71, 3, 'GUIDE'),
            ('2.5.2', 'Balancing Competing Constraints', 72, 3, 'GUIDE'),
            ('2.5.3', 'Maintaining Project Team Focus', 73, 3, 'GUIDE'),
            ('2.5.4', 'Project Communications and Engagement', 73, 3, 'GUIDE'),
            ('2.5.5', 'Managing Physical Resources', 73, 3, 'GUIDE'),
            ('2.5.6', 'Working with Procurements', 74, 3, 'GUIDE'),
            ('2.5.7', 'Monitoring New Work and Changes', 76, 3, 'GUIDE'),
            ('2.5.8', 'Learning throughout the Project', 77, 3, 'GUIDE'),
            ('2.5.9', 'Interactions with Other Performance Domains', 78, 3, 'GUIDE'),
            ('2.5.10', 'Checking Results', 79, 3, 'GUIDE'),
            
            ('2.6', 'Delivery Performance Domain', 80, 2, 'GUIDE'),
            ('2.6.1', 'Delivery of Value', 81, 3, 'GUIDE'),
            ('2.6.2', 'Deliverables', 82, 3, 'GUIDE'),
            ('2.6.3', 'Quality', 87, 3, 'GUIDE'),
            ('2.6.4', 'Suboptimal Outcomes', 91, 3, 'GUIDE'),
            ('2.6.5', 'Interactions with Other Performance Domains', 91, 3, 'GUIDE'),
            ('2.6.6', 'Checking Results', 92, 3, 'GUIDE'),
            
            ('2.7', 'Measurement Performance Domain', 93, 2, 'GUIDE'),
            ('2.7.1', 'Establishing Effective Measures', 95, 3, 'GUIDE'),
            ('2.7.2', 'What to Measure', 98, 3, 'GUIDE'),
            ('2.7.3', 'Presenting Information', 106, 3, 'GUIDE'),
            ('2.7.4', 'Measurement Pitfalls', 111, 3, 'GUIDE'),
            ('2.7.5', 'Troubleshooting Performance', 113, 3, 'GUIDE'),
            ('2.7.6', 'Growing and Improving', 114, 3, 'GUIDE'),
            ('2.7.7', 'Interactions with Other Performance Domains', 114, 3, 'GUIDE'),
            ('2.7.8', 'Checking Results', 115, 3, 'GUIDE'),
            
            ('2.8', 'Uncertainty Performance Domain', 116, 2, 'GUIDE'),
            ('2.8.1', 'General Uncertainty', 119, 3, 'GUIDE'),
            ('2.8.2', 'Ambiguity', 120, 3, 'GUIDE'),
            ('2.8.3', 'Complexity', 120, 3, 'GUIDE'),
            ('2.8.4', 'Volatility', 122, 3, 'GUIDE'),
            ('2.8.5', 'Risk', 122, 3, 'GUIDE'),
            ('2.8.6', 'Interactions with Other Performance Domains', 128, 3, 'GUIDE'),
            ('2.8.7', 'Checking Results', 129, 3, 'GUIDE'),
            
            ('3', 'TAILORING', 131, 1, 'GUIDE'),
            ('3.1', 'Overview', 131, 2, 'GUIDE'),
            ('3.2', 'Why Tailor?', 133, 2, 'GUIDE'),
            ('3.3', 'What to Tailor', 134, 2, 'GUIDE'),
            ('3.3.1', 'Life Cycle and Development Approach Selection', 134, 3, 'GUIDE'),
            ('3.3.2', 'Processes', 135, 3, 'GUIDE'),
            ('3.3.3', 'Engagement', 136, 3, 'GUIDE'),
            ('3.3.4', 'Tools', 136, 3, 'GUIDE'),
            ('3.3.5', 'Methods and Artifacts', 136, 3, 'GUIDE'),
            ('3.4', 'The Tailoring Process', 137, 2, 'GUIDE'),
            ('3.4.1', 'Select Initial Development Approach', 138, 3, 'GUIDE'),
            ('3.4.2', 'Tailor for the Organization', 139, 3, 'GUIDE'),
            ('3.4.3', 'Tailor for the Project', 141, 3, 'GUIDE'),
            ('3.5', 'Tailoring the Performance Domains', 145, 2, 'GUIDE'),
            ('3.5.1', 'Stakeholders', 147, 3, 'GUIDE'),
            ('3.5.2', 'Project Team', 147, 3, 'GUIDE'),
            ('3.5.3', 'Development Approach and Life Cycle', 148, 3, 'GUIDE'),
            ('3.5.4', 'Planning', 148, 3, 'GUIDE'),
            ('3.5.5', 'Project Work', 149, 3, 'GUIDE'),
            ('3.5.6', 'Delivery', 149, 3, 'GUIDE'),
            ('3.5.7', 'Uncertainty', 150, 3, 'GUIDE'),
            ('3.5.8', 'Measurement', 150, 3, 'GUIDE'),
            ('3.6', 'Diagnostics', 151, 2, 'GUIDE'),
            ('3.7', 'Summary', 152, 2, 'GUIDE'),
            
            ('4', 'MODELS, METHODS, AND ARTIFACTS', 153, 1, 'GUIDE'),
            ('4.1', 'Overview', 153, 2, 'GUIDE'),
            ('4.2', 'Commonly Used Models', 155, 2, 'GUIDE'),
            ('4.2.1', 'Situational Leadership Models', 155, 3, 'GUIDE'),
            ('4.2.2', 'Communication Models', 157, 3, 'GUIDE'),
            ('4.2.3', 'Motivation Models', 158, 3, 'GUIDE'),
            ('4.2.4', 'Change Models', 160, 3, 'GUIDE'),
            ('4.2.5', 'Complexity Models', 164, 3, 'GUIDE'),
            ('4.2.6', 'Project Team Development Models', 166, 3, 'GUIDE'),
            ('4.2.7', 'Other Models', 168, 3, 'GUIDE'),
            ('4.3', 'Models Applied Across Performance Domains', 172, 2, 'GUIDE'),
            ('4.4', 'Commonly Used Methods', 174, 2, 'GUIDE'),
            ('4.4.1', 'Data Gathering and Analysis', 174, 3, 'GUIDE'),
            ('4.4.2', 'Estimating', 178, 3, 'GUIDE'),
            ('4.4.3', 'Meetings and Events', 179, 3, 'GUIDE'),
            ('4.4.4', 'Other Methods', 181, 3, 'GUIDE'),
            ('4.5', 'Methods Applied Across Performance Domains', 181, 2, 'GUIDE'),
            ('4.6', 'Commonly Used Artifacts', 184, 2, 'GUIDE'),
            ('4.6.1', 'Strategy Artifacts', 184, 3, 'GUIDE'),
            ('4.6.2', 'Logs and Registers', 185, 3, 'GUIDE'),
            ('4.6.3', 'Plans', 186, 3, 'GUIDE'),
            ('4.6.4', 'Hierarchy Charts', 187, 3, 'GUIDE'),
            ('4.6.5', 'Baselines', 188, 3, 'GUIDE'),
            ('4.6.6', 'Visual Data and Information', 188, 3, 'GUIDE'),
            ('4.6.7', 'Reports', 190, 3, 'GUIDE'),
            ('4.6.8', 'Agreements and Contracts', 191, 3, 'GUIDE'),
            ('4.6.9', 'Other Artifacts', 192, 3, 'GUIDE'),
            ('4.7', 'Artifacts Applied Across Performance Domains', 192, 2, 'GUIDE'),
            
            # APPENDICES
            ('X1', 'CONTRIBUTORS AND REVIEWERS OF THE STANDARD FOR PROJECT MANAGEMENT AND A GUIDE TO THE PROJECT MANAGEMENT BODY OF KNOWLEDGE – SEVENTH EDITION', 197, 1, 'GUIDE'),
            ('X1.1', 'Contributors', 197, 2, 'GUIDE'),
            ('X1.2', 'PMI Staff', 206, 2, 'GUIDE'),
            
            ('X2', 'SPONSOR', 207, 1, 'GUIDE'),
            ('X2.1', 'Introduction', 207, 2, 'GUIDE'),
            ('X2.2', 'The Sponsor Role', 207, 2, 'GUIDE'),
            ('X2.3', 'Lack of Engagement', 208, 2, 'GUIDE'),
            ('X2.4', 'Sponsor Behaviors', 209, 2, 'GUIDE'),
            ('X2.5', 'Conclusion', 210, 2, 'GUIDE'),
            ('X2.6', 'Suggested Resources', 210, 2, 'GUIDE'),
            
            ('X3', 'THE PROJECT MANAGEMENT OFFICE', 211, 1, 'GUIDE'),
            ('X3.1', 'Introduction', 211, 2, 'GUIDE'),
            ('X3.2', 'The PMO Value Proposition—Why Have One?', 211, 2, 'GUIDE'),
            ('X3.3', 'Key PMO Capabilities', 213, 2, 'GUIDE'),
            ('X3.4', 'Evolving for Stronger Benefits Realization', 214, 2, 'GUIDE'),
            ('X3.5', 'Learn More about PMOs', 215, 2, 'GUIDE'),
            ('X3.6', 'Suggested Resources', 215, 2, 'GUIDE'),
            
            ('X4', 'PRODUCT', 217, 1, 'GUIDE'),
            ('X4.1', 'Introduction', 217, 2, 'GUIDE'),
            ('X4.2', 'Global Market Shifts', 219, 2, 'GUIDE'),
            ('X4.3', 'Impact on Project Delivery Practices', 221, 2, 'GUIDE'),
            ('X4.4', 'Organizational Considerations for Product Management', 221, 2, 'GUIDE'),
            ('X4.5', 'Summary', 225, 2, 'GUIDE'),
            ('X4.6', 'Suggested Resources', 225, 2, 'GUIDE'),
            
            ('X5', 'RESEARCH AND DEVELOPMENT FOR THE STANDARD FOR PROJECT MANAGEMENT', 227, 1, 'GUIDE'),
            ('X5.1', 'Introduction', 227, 2, 'GUIDE'),
            ('X5.2', 'The Move to a Principle-Based Standard', 227, 2, 'GUIDE'),
            ('X5.3', 'Research for The Standard for Project Management', 228, 2, 'GUIDE'),
            ('X5.4', 'Standard Development Process', 229, 2, 'GUIDE'),
            ('X5.5', 'Validating the Standard', 230, 2, 'GUIDE'),
            ('X5.6', 'Summary', 232, 2, 'GUIDE'),
        ]

        # Open PDF
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Processing: PMBOK Guide 7th Edition")
            print(f"Total pages in PDF: {len(pdf.pages)}")
            
            # Extract all pages first
            all_pages = {}
            for page_num in range(1, len(pdf.pages) + 1):
                page = pdf.pages[page_num - 1]
                text = page.extract_text()
                if text:
                    all_pages[page_num] = text
            
            # Create or get book
            book, created = Book.objects.get_or_create(
                title="PMBOK Guide 7th Edition",
                defaults={'file_path': pdf_path}
            )
            
            if not created:
                # Clear existing data for reimport
                Section.objects.filter(book=book).delete()
                Page.objects.filter(book=book).delete()
                print("Cleared existing data for reimport")
            
            # Process all sections in one book
            for idx, section_data in enumerate(sections_data):
                section_num, title, toc_page, level, part = section_data
                
                # Determine offset based on which part
                if part == 'STANDARD':
                    page_offset = STANDARD_OFFSET
                else:  # GUIDE
                    page_offset = GUIDE_OFFSET
                
                start_pdf_page = toc_page + page_offset
                
                # Find end TOC page (start of next section or end of part)
                if idx + 1 < len(sections_data):
                    next_section = sections_data[idx + 1]
                    next_toc_page = next_section[2]
                    next_part = next_section[4]
                    
                    # If next section starts on same page, this section ends on same page
                    # Otherwise it ends on page before next section
                    if next_toc_page == toc_page and next_part == part:
                        end_toc_page = toc_page
                        end_pdf_page = start_pdf_page  # Same page in PDF too!
                    else:
                        end_toc_page = next_toc_page - 1
                        # Calculate PDF end page based on part
                        if next_part == part:
                            end_pdf_page = next_toc_page + page_offset - 1
                        else:
                            # Transitioning between parts - end at last page of current part
                            if part == 'STANDARD':
                                end_pdf_page = 87  # Last PDF page of STANDARD (TOC 60 + 27)
                                end_toc_page = 60  # Last TOC page of STANDARD
                            else:
                                end_pdf_page = MAX_PDF_PAGE
                                end_toc_page = 232  # Last TOC page of GUIDE
                else:
                    # Last section
                    end_pdf_page = MAX_PDF_PAGE
                    end_toc_page = 232
                
                # Extract content for this section using pattern matching
                section_content = self.extract_section_content(
                    all_pages, section_num, start_pdf_page, end_pdf_page, sections_data, idx
                )
                
                # Create section with part prefix in section_number only (not in title)
                section = Section.objects.create(
                    book=book,
                    title=title,  # Use original title without prefix
                    section_number=f"{part[0]}{section_num}" if part == 'STANDARD' else f"G{section_num}",  # Prefix to avoid duplicates
                    level=level,
                    start_page=toc_page,
                    end_page=end_toc_page,
                    content=section_content
                )
                
                level_label = f"L{level}"
                page_display = f"Page {section.start_page}" if section.start_page == section.end_page else f"Pages {section.start_page}-{section.end_page}"
                print(f"Created: {level_label} | {section.section_number:10} | {title[:40]:40} | {page_display}")
                
                # Create page records
                for pdf_page_num in range(start_pdf_page, end_pdf_page + 1):
                    if pdf_page_num in all_pages:
                        displayed_page = pdf_page_num - page_offset
                        
                        Page.objects.get_or_create(
                            book=book,
                            page_number=displayed_page,
                            defaults={
                                'text': all_pages[pdf_page_num],
                                'section': section,
                                'topic': title
                            }
                        )
            
            print(f"\nSuccessfully imported {len(sections_data)} sections")

    def extract_section_content(self, all_pages, section_number, start_page, end_page, all_sections, current_idx):
        """Extract content for a specific section from the pages using pattern matching."""
        content_parts = []
        
        # Build pattern to find this section's start
        # Handle both regular sections (1, 1.1) and appendix sections (X1, X1.1)
        escaped_num = re.escape(section_number)
        
        # For single-digit sections (1, 2, 3), be more flexible with the pattern
        # They might appear as just the number on its own line, or with title
        if re.match(r'^\d+$', section_number) or re.match(r'^X\d+$', section_number):
            # Level 1 section - look for number alone on a line OR number followed by uppercase
            section_start_pattern = re.compile(rf'^{escaped_num}\s*$|^{escaped_num}\s+[A-Z]', re.MULTILINE)
        else:
            # Subsection - must have number followed by space and title
            section_start_pattern = re.compile(rf'^{escaped_num}\s+[A-Z]', re.MULTILINE)
        
        # Get next section number to know where to stop
        next_section_num = None
        if current_idx + 1 < len(all_sections):
            next_section_num = all_sections[current_idx + 1][0]
        
        # Build pattern for next section if it exists
        next_section_pattern = None
        if next_section_num:
            escaped_next = re.escape(next_section_num)
            if re.match(r'^\d+$', next_section_num) or re.match(r'^X\d+$', next_section_num):
                next_section_pattern = re.compile(rf'^{escaped_next}\s*$|^{escaped_next}\s+[A-Z]', re.MULTILINE)
            else:
                next_section_pattern = re.compile(rf'^{escaped_next}\s+[A-Z]', re.MULTILINE)
        
        found_start = False
        
        for page_num in range(start_page, end_page + 1):
            if page_num not in all_pages:
                continue
            
            page_text = all_pages[page_num]
            
            if not found_start:
                # Look for section start on this page
                match = section_start_pattern.search(page_text)
                if match:
                    # Found the section start
                    found_start = True
                    remaining_text = page_text[match.start():]
                    
                    # Check if next section is on same page
                    if next_section_pattern:
                        next_match = next_section_pattern.search(remaining_text)
                        if next_match:
                            # Next section on same page, only take content before it
                            content_parts.append(remaining_text[:next_match.start()])
                            break
                    
                    content_parts.append(remaining_text)
                # If not found yet, skip this page
            else:
                # Already found start, check if next section starts on this page
                if next_section_pattern:
                    next_match = next_section_pattern.search(page_text)
                    if next_match:
                        # Next section starts here, take content before it
                        content_parts.append(page_text[:next_match.start()])
                        break
                
                # No next section on this page, take all content
                content_parts.append(page_text)
        
        full_content = '\n\n'.join(content_parts)
        return full_content.strip()
