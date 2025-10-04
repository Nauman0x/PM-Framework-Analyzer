import pdfplumber
import re

pdf_path = r"d:\Proj Management\Managing Successful Projects with PRINCE2® -- Andy Murray -- 7, 2023 -- PeopleCert International Limited.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages in PDF: {len(pdf.pages)}")
    print("\nSearching for actual chapter 1 content (not TOC)...")
    print("="*80)
    
    for i, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ''
        
        # Look for "1.3 What is a project?" followed by actual paragraph content
        # Not just the TOC line
        if re.search(r'^1\.3\s+What is a project\?', text, re.MULTILINE):
            # Check if this looks like actual content (has more than just the title line)
            lines = text.split('\n')
            content_lines = [l for l in lines if l.strip()]
            if len(content_lines) > 20:  # Actual content page will have many lines
                print(f"\nFound actual content for '1.3 What is a project?' on PDF page {i}")
                print(f"TOC says it's on page 5")
                print(f"Offset: {i - 5} pages")
                print(f"\nContent preview:")
                print(text[:800])
                break
