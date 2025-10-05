import pdfplumber
import re

fpath = r"d:\Proj Management\ISO 21500-2021_ Project, programme and portfolio management - Context and concepts.pdf"

with pdfplumber.open(fpath) as pdf:
    # Check pages that should have main headings based on TOC
    test_pages = [7, 10, 11, 15]  # Pages with section 4, 4.2, 4.3, 5.2 according to TOC
    
    for page_num in test_pages:
        if page_num <= len(pdf.pages):
            page = pdf.pages[page_num - 1]
            print(f"\n{'='*70}")
            print(f"PAGE {page_num}")
            print('='*70)
            
            # Get text
            text = page.extract_text() or ''
            lines = [l.strip() for l in text.splitlines() if l.strip()]
            
            # Show first 15 lines
            for i, line in enumerate(lines[:15], 1):
                # Check if line matches section number pattern
                match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+)$', line)
                marker = " <-- SECTION?" if match else ""
                print(f"{i:2}. {line[:70]}{marker}")
            
            # Get character info for font sizes
            chars = page.chars
            if chars:
                print(f"\nFont sizes found: {set(round(c.get('size', 0), 1) for c in chars[:100])}")
