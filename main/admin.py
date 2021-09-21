from django.contrib import admin
from .models import StudentClass, StudentSubject, StudentChapter, StudentSection

# Register your models here.

# class BookAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ("Main", {"fields": ["book_title", "book_description"]}),
#         ("Extra", {"fields": ["book_published"]}),
#     ]
# admin.site.register(Book, BookAdmin)

admin.site.register(StudentClass)
admin.site.register(StudentSubject)
admin.site.register(StudentChapter)
admin.site.register(StudentSection)
