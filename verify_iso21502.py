import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdfcompare.settings')
django.setup()

from library.models import Book, Section

# Get ISO 21502 book
book = Book.objects.get(title__contains="ISO 21502")
print(f"Book: {book.title}")
print(f"Book ID: {book.id}")
print(f"Total sections: {book.sections.count()}\n")

# Check a few sample sections
test_sections = [
    "1",      # Scope
    "4.1.1",  # General (subsection)
    "7.2.1",  # Planning - Overview (deep subsection)
    "7.8.2",  # Risk management - Identifying risk
]

for sec_num in test_sections:
    try:
        sec = book.sections.get(section_number=sec_num)
        content_preview = sec.content[:200] if sec.content else "(No content)"
        print(f"Section {sec_num}: {sec.title}")
        print(f"  Pages: {sec.start_page}-{sec.end_page}")
        print(f"  Level: {sec.level}")
        print(f"  Content length: {len(sec.content) if sec.content else 0} chars")
        print(f"  Preview: {content_preview}...")
        print()
    except Section.DoesNotExist:
        print(f"Section {sec_num} not found!\n")

# Check sections on page 7 (should have Scope, Normative refs, Terms & defs)
print("\n=== Sections on Page 7 ===")
sections_page7 = book.sections.filter(start_page__lte=7, end_page__gte=7).order_by('section_number')
for sec in sections_page7:
    print(f"{sec.section_number:8} | {sec.title[:40]:40} | Content: {len(sec.content) if sec.content else 0} chars")
