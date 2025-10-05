import pdfplumber
import re

pdf_path = r"d:\Proj Management\Project-Management-Institute-A-Guide-to-the-Project-Management-Body-of-Knowledge-PMBOK-R-Guide-PMBOK®️-Guide-Project-Management-Institute-2021.pdf"

sections_found = []

# The TOC shows we have two main parts:
# - THE STANDARD FOR PROJECT MANAGEMENT (pages 1-60)
# - A GUIDE TO THE PROJECT MANAGEMENT BODY OF KNOWLEDGE (starts at page 1 again)
# We need to find the page offset first

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages in PDF: {len(pdf.pages)}")
    
    # Let's check a few pages to find the offset
    # From TOC, "1 INTRODUCTION" should be on page 3 of "THE STANDARD"
    print("\n=== Checking for page offset ===")
    for i in range(1, 30):  # Check first 30 PDF pages
        page = pdf.pages[i-1]
        text = page.extract_text()
        if text and "1 INTRODUCTION" in text and "Purpose of The Standard for Project Management" in text:
            print(f"Found 'THE STANDARD' Introduction on PDF page {i}")
            print(f"Page offset for THE STANDARD = {i - 3}")
            standard_offset = i - 3
            break
    
    # Now scan for all sections
    # Pattern: section numbers like "1", "1.1", "1.1.1", "1.2.3", etc.
    # followed by title text
    pattern = re.compile(r'^(\d+(?:\.\d+){0,3})\s+([A-Z][^\n]+?)(?:\s+\.{2,}|\s+\d+)?\s*$', re.MULTILINE)
    
    # Scan THE STANDARD FOR PROJECT MANAGEMENT (approximate pages)
    print("\n=== Scanning THE STANDARD FOR PROJECT MANAGEMENT ===")
    for page_num in range(1, 70):  # Approximate range
        try:
            page = pdf.pages[page_num - 1]
            text = page.extract_text()
            if not text:
                continue
            
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                # Match section patterns
                match = re.match(r'^(\d+(?:\.\d+){0,3})\s+([A-Z][^\n]+?)(?:\s+\.{2,}|\s+\d+)?\s*$', line)
                if match:
                    section_num = match.group(1)
                    title = match.group(2).strip()
                    
                    # Clean up title
                    title = re.sub(r'\s+\.{2,}.*$', '', title)  # Remove dots
                    title = re.sub(r'\s+\d+\s*$', '', title)  # Remove trailing page numbers
                    
                    # Skip if it's just dots or numbers
                    if title and not re.match(r'^[\d\.\s]+$', title):
                        sections_found.append((section_num, title, page_num, 'STANDARD'))
        except Exception as e:
            pass
    
    # Scan A GUIDE TO THE PMBOK (starts around page 70+)
    print("\n=== Scanning A GUIDE TO THE PMBOK ===")
    for page_num in range(70, len(pdf.pages) + 1):
        try:
            page = pdf.pages[page_num - 1]
            text = page.extract_text()
            if not text:
                continue
            
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                # Match section patterns
                match = re.match(r'^(\d+(?:\.\d+){0,3})\s+([A-Z][^\n]+?)(?:\s+\.{2,}|\s+\d+)?\s*$', line)
                if match:
                    section_num = match.group(1)
                    title = match.group(2).strip()
                    
                    # Clean up title
                    title = re.sub(r'\s+\.{2,}.*$', '', title)
                    title = re.sub(r'\s+\d+\s*$', '', title)
                    
                    if title and not re.match(r'^[\d\.\s]+$', title):
                        sections_found.append((section_num, title, page_num, 'GUIDE'))
        except Exception as e:
            pass

# Remove duplicates and sort
seen = set()
unique_sections = []
for item in sections_found:
    key = (item[0], item[3])  # section_num + book part
    if key not in seen:
        seen.add(key)
        unique_sections.append(item)

# Print sections grouped by part
print("\n=== THE STANDARD FOR PROJECT MANAGEMENT ===")
standard_sections = [s for s in unique_sections if s[3] == 'STANDARD']
for section_num, title, page, part in sorted(standard_sections, key=lambda x: [int(n) for n in x[0].split('.')]):
    level = len(section_num.split('.'))
    indent = "  " * (level - 1)
    print(f"{indent}('{section_num}', '{title}', {page}, {level}),")

print(f"\nTotal STANDARD sections found: {len(standard_sections)}")

print("\n=== A GUIDE TO THE PMBOK ===")
guide_sections = [s for s in unique_sections if s[3] == 'GUIDE']
for section_num, title, page, part in sorted(guide_sections, key=lambda x: [int(n) for n in x[0].split('.')]):
    level = len(section_num.split('.'))
    indent = "  " * (level - 1)
    print(f"{indent}('{section_num}', '{title}', {page}, {level}),")

print(f"\nTotal GUIDE sections found: {len(guide_sections)}")
print(f"\nGrand total sections: {len(unique_sections)}")
