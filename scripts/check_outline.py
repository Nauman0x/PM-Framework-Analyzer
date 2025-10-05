import pdfplumber
import json

fpath = r"d:\Proj Management\ISO 21500-2021_ Project, programme and portfolio management - Context and concepts.pdf"

with pdfplumber.open(fpath) as pdf:
    print(f"Total pages: {len(pdf.pages)}\n")
    
    outlines = pdf.outlines or []
    print(f"Number of outline entries: {len(outlines)}\n")
    
    def show_outline(items, level=0):
        for item in items[:30]:  # Show first 30
            if isinstance(item, dict):
                title = item.get('title', '')
                page = item.get('page')
                page_number = item.get('page_number')
                indent = "  " * level
                print(f"{indent}{title} -> page={page}, page_number={page_number}")
                children = item.get('children', [])
                if children:
                    show_outline(children, level + 1)
    
    print("Outline structure:")
    print("-" * 60)
    show_outline(outlines)
