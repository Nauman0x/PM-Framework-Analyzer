import pdfplumber

pdf_path = r"d:\Proj Management\Project-Management-Institute-A-Guide-to-the-Project-Management-Body-of-Knowledge-PMBOK-R-Guide-PMBOK®️-Guide-Project-Management-Institute-2021.pdf"

with pdfplumber.open(pdf_path) as pdf:
    all_pages = {}
    for page_num in range(1, len(pdf.pages) + 1):
        page = pdf.pages[page_num - 1]
        text = page.extract_text()
        if text:
            all_pages[page_num] = text
    
    print(f"Total pages loaded: {len(all_pages)}")
    print(f"Page 30 exists: {30 in all_pages}")
    if 30 in all_pages:
        print(f"Page 30 length: {len(all_pages[30])} chars")
        print(f"Page 30 preview: {all_pages[30][:200]}")
