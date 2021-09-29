from django.contrib import admin
from .models import StudentClass, StudentSubject, StudentChapter, StudentSection, UploadImage, UploadVideo, UploadAudio, UploadFile
from django.db import models
from tinymce.widgets import TinyMCE

# Register your models here.

# class BookAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ("Main", {"fields": ["book_title", "book_description"]}),
#         ("Extra", {"fields": ["book_published"]}),
#     ]
# admin.site.register(Book, BookAdmin)

class StudentSectionAdmin(admin.ModelAdmin):
   formfield_overrides = {models.TextField: {'widget': TinyMCE()}}

admin.site.register(StudentClass)
admin.site.register(StudentSubject)
admin.site.register(StudentChapter)
admin.site.register(StudentSection, StudentSectionAdmin)

admin.site.register(UploadImage)
admin.site.register(UploadVideo)
admin.site.register(UploadAudio)
admin.site.register(UploadFile)
