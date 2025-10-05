import pdfplumber
import re

# Simulate the extract_section_content method
def extract_section_content(all_pages, section_number, start_page, end_page, all_sections, current_idx):
    """Extract content for a specific section from the pages using pattern matching."""
    content_parts = []
    
    # Build pattern to find this section's start
    escaped_num = re.escape(section_number)
    
    # For single-digit sections (1, 2, 3), be more flexible with the pattern
    if re.match(r'^\d+$', section_number) or re.match(r'^X\d+$', section_number):
        section_start_pattern = re.compile(rf'^{escaped_num}\s*$|^{escaped_num}\s+[A-Z]', re.MULTILINE)
    else:
        section_start_pattern = re.compile(rf'^{escaped_num}\s+[A-Z]', re.MULTILINE)
    
    # Get next section number
    next_section_num = None
    if current_idx + 1 < len(all_sections):
        next_section_num = all_sections[current_idx + 1][0]
    
    # Build pattern for next section
    next_section_pattern = None
    if next_section_num:
        escaped_next = re.escape(next_section_num)
        if re.match(r'^\d+$', next_section_num) or re.match(r'^X\d+$', next_section_num):
            next_section_pattern = re.compile(rf'^{escaped_next}\s*$|^{escaped_next}\s+[A-Z]', re.MULTILINE)
        else:
            next_section_pattern = re.compile(rf'^{escaped_next}\s+[A-Z]', re.MULTILINE)
    
    found_start = False
    
    print(f"\nDEBUG: Extracting section '{section_number}'")
    print(f"  Pages: {start_page} to {end_page}")
    print(f"  Next section: {next_section_num}")
    
    for page_num in range(start_page, end_page + 1):
        if page_num not in all_pages:
            print(f"  Page {page_num}: NOT in all_pages")
            continue
        
        page_text = all_pages[page_num]
        print(f"  Page {page_num}: {len(page_text)} chars")
        
        if not found_start:
            match = section_start_pattern.search(page_text)
            if match:
                found_start = True
                remaining_text = page_text[match.start():]
                print(f"    Found section start at position {match.start()}")
                
                if next_section_pattern:
                    next_match = next_section_pattern.search(remaining_text)
                    if next_match:
                        print(f"    Found next section at position {next_match.start()} in remaining")
                        content_parts.append(remaining_text[:next_match.start()])
                        break
                
                content_parts.append(remaining_text)
            else:
                print(f"    Section start NOT found")
        else:
            if next_section_pattern:
                next_match = next_section_pattern.search(page_text)
                if next_match:
                    content_parts.append(page_text[:next_match.start()])
                    break
            
            content_parts.append(page_text)
    
    full_content = '\n\n'.join(content_parts)
    print(f"  Final content: {len(full_content)} chars")
    return full_content.strip()

# Load PDF
pdf_path = r"d:\Proj Management\Project-Management-Institute-A-Guide-to-the-Project-Management-Body-of-Knowledge-PMBOK-R-Guide-PMBOK®️-Guide-Project-Management-Institute-2021.pdf"

all_pages = {}
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages, 1):
        all_pages[i] = page.extract_text()

# Simulate extracting section 1
sections_data = [
    ('1', 'INTRODUCTION', 3, 1, 'STANDARD'),
    ('1.1', 'Purpose of The Standard for Project Management', 3, 2, 'STANDARD'),
]

content = extract_section_content(all_pages, '1', 30, 30, sections_data, 0)
print(f"\n{'='*60}")
print(f"EXTRACTED CONTENT:")
print(f"{'='*60}")
print(content)
