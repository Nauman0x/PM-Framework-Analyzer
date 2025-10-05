import pdfplumber

pdf_path = r"d:\Proj Management\Managing Successful Projects with PRINCE2® -- Andy Murray -- 7, 2023 -- PeopleCert International Limited.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages in PDF: {len(pdf.pages)}")
    print("\nScanning pages to find actual content...")
    print("="*80)
    
    # Check pages around where we expect content to start
    for i in range(15, 35):  # Check pages 15-35
        page = pdf.pages[i-1]
        text = page.extract_text() or ''
        
        # Look for "1 Introduction" at start of actual chapter content
        # It should be followed by actual paragraph text, not TOC entries
        if '1 Introduction' in text:
            # Check if followed by actual content (look for common words like "this", "chapter", etc.)
            if any(word in text.lower() for word in ['this document', 'this book', 'prince2 is', 'project management']):
                print(f"\nPDF page {i} - Found chapter 1:")
                print(text[:1000])
                print(f"\n---\nIf TOC page 1 maps to PDF page {i}, offset is {i-1}")
                break
