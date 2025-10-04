import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdfcompare.settings')
django.setup()

from library.models import Book, Section

# Get ISO 21502 book
book = Book.objects.get(title__contains="ISO 21502")

# Check section 4.2.3 - Customer and supplier perspective
sec_423 = book.sections.get(section_number="4.2.3")
print(f"Section: {sec_423.section_number} - {sec_423.title}")
print(f"Pages: {sec_423.start_page}-{sec_423.end_page}")
print(f"Content length: {len(sec_423.content) if sec_423.content else 0} chars")
print(f"\nContent preview (first 500 chars):")
print(sec_423.content[:500] if sec_423.content else "(No content)")
print("\n" + "="*80 + "\n")

# Check section 4.1.2 - Projects  
sec_412 = book.sections.get(section_number="4.1.2")
print(f"Section: {sec_412.section_number} - {sec_412.title}")
print(f"Pages: {sec_412.start_page}-{sec_412.end_page}")
print(f"Content length: {len(sec_412.content) if sec_412.content else 0} chars")
print(f"\nContent preview (first 500 chars):")
print(sec_412.content[:500] if sec_412.content else "(No content)")

