from django.db import models
from datetime import datetime

from django.core.exceptions import ValidationError

# Create your models here.

class StudentClass(models.Model):
    student_class = models.CharField(max_length=100)
    class_summary = models.CharField(max_length=500)
    # Image/Media to be added later
    class_slug = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Classes"

    def validate_unique(self, *args, **kwargs):
        super(StudentClass, self).validate_unique(*args, **kwargs)
        if self.__class__.objects.filter(class_slug=self.class_slug).exists():
            raise ValidationError(message=f'StudentClass with (class_slug=\"{self.class_slug}\") already exists.',
                                  code='unique_together',)

    def __str__(self):
        return self.student_class

class StudentSubject(models.Model):
    student_subject = models.CharField(max_length=100)
    subject_summary = models.CharField(max_length=500)
    # Image/Media to be added later
    subject_slug = models.CharField(max_length=100)

    student_class = models.ForeignKey(StudentClass, default=1, verbose_name="Class", on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name_plural = "Subjects"

    def validate_unique(self, *args, **kwargs):
        super(StudentSubject, self).validate_unique(*args, **kwargs)
        if self.__class__.objects.filter(subject_slug=self.subject_slug, student_class__class_slug=self.student_class.class_slug).exists():
            raise ValidationError(message=f'StudentSubject with (class_slug=\"{self.student_class.class_slug}\", subject_slug=\"{self.subject_slug}\") already exists.',
                                  code='unique_together',)

    def __str__(self):
        return self.student_subject

class StudentChapter(models.Model):
    student_chapter = models.CharField(max_length=100)
    chapter_summary = models.CharField(max_length=500)
    # Image/Media to be added later
    chapter_slug = models.CharField(max_length=100)

    student_subject = models.ForeignKey(StudentSubject, default=1, verbose_name="Subject", on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name_plural = "Chapters"

    def validate_unique(self, *args, **kwargs):
        super(StudentChapter, self).validate_unique(*args, **kwargs)
        if self.__class__.objects.filter(chapter_slug=self.chapter_slug, student_subject__subject_slug=self.student_subject.subject_slug, student_subject__student_class__class_slug=self.student_subject.student_class.class_slug).exists():
            raise ValidationError(message=f'StudentChapter with (class_slug=\"{self.student_subject.student_class.class_slug}\", subject_slug=\"{self.student_subject.subject_slug}\", chapter_slug=\"{self.chapter_slug}\") already exists.',
                                  code='unique_together',)

    def __str__(self):
        return self.student_chapter

class StudentSection(models.Model):
    student_section = models.CharField(max_length=100)
    section_summary = models.CharField(max_length=500)
    # Image/Media to be added later
    section_slug = models.CharField(max_length=100)

    section_text = models.CharField(max_length=1000)

    student_chapter = models.ForeignKey(StudentChapter, default=1, verbose_name="Chapter", on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name_plural = "Sections"

    def validate_unique(self, *args, **kwargs):
        super(StudentSection, self).validate_unique(*args, **kwargs)
        if self.__class__.objects.filter(section_slug=self.section_slug, student_chapter__chapter_slug=self.student_chapter.chapter_slug, student_chapter__student_subject__subject_slug=self.student_chapter.student_subject.subject_slug, student_chapter__student_subject__student_class__class_slug=self.student_chapter.student_subject.student_class.class_slug).exists():
            raise ValidationError(message=f'StudentSection with (class_slug=\"{self.student_chapter.student_subject.student_class.class_slug}\", subject_slug=\"{self.student_chapter.student_subject.subject_slug}\", chapter_slug=\"{self.student_chapter.chapter_slug}\", section_slug=\"{self.section_slug}\") already exists.',
                                  code='unique_together',)

    def __str__(self):
        return self.student_section

class Book(models.Model):
    book_title = models.CharField(max_length=100)
    book_description = models.TextField()
    book_published = models.DateTimeField("When was this book published?", default=datetime.now())

    def __str__(self):
        return self.book_title
