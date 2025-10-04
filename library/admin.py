from django.contrib import admin
from .models import Book, Page
from .models import Section

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_path')


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('book', 'page_number', 'topic')
    search_fields = ('text', 'topic')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('book', 'section_number', 'title', 'start_page', 'end_page')
    search_fields = ('title', 'section_number')
