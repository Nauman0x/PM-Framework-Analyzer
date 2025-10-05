import pdfplumber
import re

# Test content extraction from PMBOK PDF
pdf_path = r"d:\Proj Management\Project-Management-Institute-A-Guide-to-the-Project-Management-Body-of-Knowledge-PMBOK-R-Guide-PMBOK®️-Guide-Project-Management-Institute-2021.pdf"

with pdfplumber.open(pdf_path) as pdf:
    # Check PDF page 30 (where section 1 INTRODUCTION should be)
    page = pdf.pages[29]  # 0-indexed
    text = page.extract_text()
    
    print("="*60)
    print("PDF PAGE 30 (STANDARD Section 1)")
    print("="*60)
    
    # Find section 1 start
    section_1_pattern = re.compile(r'^1\s*$|^1\s+[A-Z]', re.MULTILINE)
    match_1 = section_1_pattern.search(text)
    
    if match_1:
        print(f"Section 1 starts at position {match_1.start()}")
        remaining = text[match_1.start():]
        
        # Find section 1.1 start (next section)
        section_1_1_pattern = re.compile(r'^1\.1\s+[A-Z]', re.MULTILINE)
        match_1_1 = section_1_1_pattern.search(remaining)
        
        if match_1_1:
            print(f"Section 1.1 starts at position {match_1_1.start()} in remaining text")
            content_1 = remaining[:match_1_1.start()]
            print(f"\nExtracted content for Section 1 ({len(content_1)} chars):")
            print(content_1)
        else:
            print("\nSection 1.1 NOT FOUND on this page")
            print(f"\nAll remaining text ({len(remaining)} chars):")
            print(remaining)
    else:
        print("Section 1 NOT FOUND!")
