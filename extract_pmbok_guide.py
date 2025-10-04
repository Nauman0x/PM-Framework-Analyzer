import pdfplumber
import re

pdf_path = r"d:\Proj Management\Project-Management-Institute-A-Guide-to-the-Project-Management-Body-of-Knowledge-PMBOK-R-Guide-PMBOK®️-Guide-Project-Management-Institute-2021.pdf"

sections_found = []

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages in PDF: {len(pdf.pages)}")
    
    # Find the offset for THE GUIDE section (A GUIDE TO THE PMBOK starts around page 88)
    print("\n=== Checking for page offset ===")
    for i in range(80, 100):
        page = pdf.pages[i-1]
        text = page.extract_text()
        if text and "1. INTRODUCTION" in text and "PMBOK" in text:
            print(f"Found 'THE GUIDE' Introduction on PDF page {i}")
            print(f"Page offset for THE GUIDE = {i - 3}")
            guide_offset = i - 3
            break
    
    # Scan A GUIDE TO THE PMBOK section
    # Pattern: section numbers including X notation for appendices
    print("\n=== Scanning A GUIDE TO THE PMBOK ===")
    for page_num in range(88, len(pdf.pages) + 1):
        try:
            page = pdf.pages[page_num - 1]
            text = page.extract_text()
            if not text:
                continue
            
            lines = text.split('\n')
            for i, line in enumerate(lines):
                line = line.strip()
                
                # Match regular sections (1, 1.1, 1.1.1, 1.1.1.1)
                match = re.match(r'^(\d+(?:\.\d+){0,4})\s+([A-Z][^\n]+?)(?:\s+\.{2,}|\s+\d+)?\s*$', line)
                if match:
                    section_num = match.group(1)
                    title = match.group(2).strip()
                    
                    # Clean up title
                    title = re.sub(r'\s+\.{2,}.*$', '', title)
                    title = re.sub(r'\s+\d+\s*$', '', title)
                    
                    if title and not re.match(r'^[\d\.\s]+$', title) and len(title) > 3:
                        sections_found.append((section_num, title, page_num))
                
                # Match appendix sections (X1, X1.1, etc.)
                match = re.match(r'^(X\d+(?:\.\d+)?)\s+([A-Z][^\n]+?)(?:\s+\.{2,}|\s+\d+)?\s*$', line)
                if match:
                    section_num = match.group(1)
                    title = match.group(2).strip()
                    
                    # Clean up title
                    title = re.sub(r'\s+\.{2,}.*$', '', title)
                    title = re.sub(r'\s+\d+\s*$', '', title)
                    
                    if title and not re.match(r'^[\d\.\s]+$', title) and len(title) > 3:
                        sections_found.append((section_num, title, page_num))
        except Exception as e:
            pass

# Remove duplicates
seen = set()
unique_sections = []
for item in sections_found:
    key = item[0]  # section_num
    if key not in seen:
        seen.add(key)
        unique_sections.append(item)

# Sort sections
def sort_key(item):
    section_num = item[0]
    if section_num.startswith('X'):
        # Appendix sections - sort separately
        parts = section_num[1:].split('.')
        return (999, int(parts[0])) + tuple(int(p) for p in parts[1:]) + (0,) * (5 - len(parts))
    else:
        parts = section_num.split('.')
        return tuple(int(p) for p in parts) + (0,) * (5 - len(parts))

sorted_sections = sorted(unique_sections, key=sort_key)

# Print as Python code
print("\n# A GUIDE TO THE PMBOK sections_data:")
print("sections_data = [")
for section_num, title, page in sorted_sections:
    level = len(section_num.replace('X', '').split('.'))
    if section_num.startswith('X'):
        # Appendix sections
        if '.' in section_num:
            level = 2  # X1.1, X1.2, etc.
        else:
            level = 1  # X1, X2, etc.
    
    indent = "    " * level
    print(f"{indent}('{section_num}', '{title}', {page}, {level}, 'GUIDE'),")

print("]")
print(f"\nTotal sections found: {len(sorted_sections)}")
