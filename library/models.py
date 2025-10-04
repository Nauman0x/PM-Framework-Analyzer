from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=1024)
    file_path = models.CharField(max_length=2048)

    def __str__(self):
        return self.title


class Page(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='pages')
    page_number = models.IntegerField()
    text = models.TextField()
    topic = models.CharField(max_length=256, blank=True, null=True)
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True, blank=True, related_name='pages')

    class Meta:
        unique_together = ('book', 'page_number')

    def __str__(self):
        return f"{self.book.title} - page {self.page_number}"


class Section(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=1024)
    section_number = models.CharField(max_length=64, blank=True, null=True)
    level = models.IntegerField(default=1)
    start_page = models.IntegerField()
    end_page = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True, default='')

    class Meta:
        ordering = ('book', 'start_page')

    def __str__(self):
        num = f"{self.section_number} " if self.section_number else ''
        return f"{self.book.title} - {num}{self.title} ({self.start_page}-{self.end_page or '?'})"
