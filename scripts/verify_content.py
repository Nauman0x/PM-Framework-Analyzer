import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdfcompare.settings')
django.setup()

from library.models import Book, Section

book = Book.objects.first()
if book:
    print(f'\nBook: {book.title}')
    print(f'URL: http://127.0.0.1:8000/book/{book.id}/')
    print('\n' + '='*80)
    
    # Check a few sections
    test_sections = ['1', '2', '3', '4.2', '5.2.1']
    
    for secnum in test_sections:
        sec = book.sections.filter(section_number=secnum).first()
        if sec:
            print(f'\nSection {sec.section_number}: {sec.title}')
            print(f'Pages: {sec.start_page}-{sec.end_page}')
            print(f'Content length: {len(sec.content)} characters')
            print(f'First 200 chars: {sec.content[:200]}...')
            print('-'*80)
