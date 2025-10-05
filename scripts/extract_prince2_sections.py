import pdfplumber
import re

pdf_path = r"d:\Proj Management\Managing Successful Projects with PRINCE2® -- Andy Murray -- 7, 2023 -- PeopleCert International Limited.pdf"

# We know the offset is 19 pages (TOC page 1 = PDF page 20)
PAGE_OFFSET = 19

sections_found = []

with pdfplumber.open(pdf_path) as pdf:
    # Scan from page 20 (TOC page 1) to page 302 (TOC page 283)
    for pdf_page_num in range(20, min(303, len(pdf.pages) + 1)):
        page = pdf.pages[pdf_page_num - 1]
        text = page.extract_text() or ''
        
        # Look for section numbers at the start of lines
        # Pattern: start of line, section number (1, 1.1, 1.1.1, etc.), space, then title starting with uppercase
        pattern = r'^(\d+(?:\.\d+){0,2})\s+([A-Z][^\n]+?)(?:\s+\d+)?$'
        
        for match in re.finditer(pattern, text, re.MULTILINE):
            section_num = match.group(1)
            title = match.group(2).strip()
            
            # Calculate TOC page number
            toc_page = pdf_page_num - PAGE_OFFSET
            
            # Determine level based on dots in section number
            level = section_num.count('.') + 1
            
            # Filter out noise (single letters, very short titles, etc.)
            if len(title) > 3 and not title.startswith('CHAPTER'):
                sections_found.append({
                    'number': section_num,
                    'title': title,
                    'page': toc_page,
                    'level': level
                })

# Remove duplicates and sort by section number
seen = set()
unique_sections = []
for sec in sections_found:
    key = (sec['number'], sec['title'][:30])
    if key not in seen:
        seen.add(key)
        unique_sections.append(sec)

# Sort by section number (convert to tuple of integers for proper sorting)
def section_key(s):
    parts = s['number'].split('.')
    return tuple(int(p) for p in parts)

unique_sections.sort(key=section_key)

# Print in Python format for import script
print("sections_data = [")
for sec in unique_sections:
    # Limit to first 283 pages as per TOC
    if sec['page'] <= 283:
        print(f"    ('{sec['number']}', '{sec['title'][:60]}', {sec['page']}, {sec['level']}),")
print("]")

print(f"\n\nTotal sections found: {len([s for s in unique_sections if s['page'] <= 283])}")
