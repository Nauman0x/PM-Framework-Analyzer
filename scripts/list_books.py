import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdfcompare.settings')
django.setup()

from library.models import Book

books = Book.objects.all()
print(f'\nBooks in database:')
print('='*60)
for b in books:
    print(f'ID: {b.id} | {b.title}')
    print(f'   URL: http://127.0.0.1:8000/book/{b.id}/')
    print()
