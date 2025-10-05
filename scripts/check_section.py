import pdfplumber
import re

pdf_path = r"d:\Proj Management\Project-Management-Institute-A-Guide-to-the-Project-Management-Body-of-Knowledge-PMBOK-R-Guide-PMBOK®️-Guide-Project-Management-Institute-2021.pdf"

with pdfplumber.open(pdf_path) as pdf:
    # Section 2 "A SYSTEM FOR VALUE DELIVERY" is on TOC page 7, PDF page 34 (7+27)
    page_34 = pdf.pages[33].extract_text()
    
    print("="*60)
    print("PDF PAGE 34 (TOC page 7) - Section 2")
    print("="*60)
    print(page_34)
    
    print("\n" + "="*60)
    print("Testing pattern matching")
    print("="*60)
    
    # Pattern for section 2
    pattern_2 = re.compile(r'^2\s*$|^2\s+[A-Z]', re.MULTILINE)
    match_2 = pattern_2.search(page_34)
    print(f"Section 2 found: {match_2 is not None}")
    if match_2:
        print(f"Position: {match_2.start()}")
        print(f"Match text: {page_34[match_2.start():match_2.start()+50]}")
        
    # Pattern for section 2.1
    pattern_21 = re.compile(r'^2\.1\s+[A-Z]', re.MULTILINE)
    match_21 = pattern_21.search(page_34)
    print(f"\nSection 2.1 found: {match_21 is not None}")
    if match_21:
        print(f"Position: {match_21.start()}")
        
        # Extract content between section 2 and 2.1
        if match_2:
            content = page_34[match_2.start():match_21.start()]
            print(f"\nContent between 2 and 2.1 ({len(content)} chars):")
            print(content)
