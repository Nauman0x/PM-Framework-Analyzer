import pdfplumber

pdf_path = r"d:\Proj Management\Managing Successful Projects with PRINCE2® -- Andy Murray -- 7, 2023 -- PeopleCert International Limited.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages in PDF: {len(pdf.pages)}")
    
    # Check specific pages
    for page_num in [18, 19, 20, 21, 22, 23, 24, 25]:
        page = pdf.pages[page_num-1]
        text = page.extract_text() or ''
        print(f"\n{'='*80}")
        print(f"PDF Page {page_num}:")
        print(f"{'='*80}")
        print(text[:500])
        print("...")
