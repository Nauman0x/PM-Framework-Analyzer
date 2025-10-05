import pdfplumber

pdf_path = r"d:\Proj Management\ISO 21502-2020_ Project, programme and portfolio management - Guidance on project management.pdf"

with pdfplumber.open(pdf_path) as pdf:
    # Check page 13 (index 12) - should have section 4.2.3
    page = pdf.pages[12]
    text = page.extract_text()
    
    print("=== PAGE 13 CONTENT (Section 4.2.3) ===")
    print(text)
    print("\n" + "="*80 + "\n")
    
    # Check page 11 (index 10) - should have section 4.1.2
    page11 = pdf.pages[10]
    text11 = page11.extract_text()
    print("=== PAGE 11 CONTENT (Section 4.1.2) ===")
    print(text11[:1000])
