import pdfplumber
import re

pdf_path = r"d:\Proj Management\ISO 21502-2020_ Project, programme and portfolio management - Guidance on project management.pdf"

with pdfplumber.open(pdf_path) as pdf:
    # Search for section 4.2.3
    print("Searching for '4.2.3' in the PDF...")
    print("="*80)
    
    for i, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ''
        
        # Look for section 4.2.3
        if re.search(r'\b4\.2\.3\b', text):
            print(f"\nFound '4.2.3' on PDF page {i}")
            # Extract context around it
            match = re.search(r'(.{0,200}\b4\.2\.3\b.{0,300})', text, re.DOTALL)
            if match:
                print(f"Context: {match.group(1)}")
                print("-"*80)
