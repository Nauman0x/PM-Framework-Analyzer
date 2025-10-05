import pdfplumber

pdf_path = r"d:\Proj Management\ISO 21500-2021_ Project, programme and portfolio management - Context and concepts.pdf"

with pdfplumber.open(pdf_path) as pdf:
    # The TOC says "1 Scope" is on page 1
    # Let's find where it actually is in the PDF
    print("Searching for '1 Scope' in ISO 21500...")
    print("="*80)
    
    for i, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ''
        
        # Look for "1 Scope" at the start of the content
        if '1 Scope' in text:
            print(f"\nFound '1 Scope' on PDF page {i}")
            print(f"TOC says it's on page 1")
            print(f"Offset: {i - 1} pages")
            print(f"\nContent preview:")
            print(text[:500])
            break
