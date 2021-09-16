from django.contrib import admin
from .models import Book

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Main", {"fields": ["book_title", "book_description"]}),
        ("Extra", {"fields": ["book_published"]}),
    ]

admin.site.register(Book, BookAdmin)
