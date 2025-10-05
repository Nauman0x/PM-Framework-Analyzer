import pdfplumber

pdf_path = r"d:\Proj Management\Managing Successful Projects with PRINCE2® -- Andy Murray -- 7, 2023 -- PeopleCert International Limited.pdf"

with pdfplumber.open(pdf_path) as pdf:
    # TOC page 5 = PDF page 8 (offset of 3)
    page = pdf.pages[7]  # 0-indexed, so page 8 is index 7
    text = page.extract_text()
    
    print("Page 8 (TOC page 5) - Should contain '1.3 What is a project?':")
    print("="*80)
    print(text[:1000])
