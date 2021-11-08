from django.db import models
from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.conf import settings
from os.path import splitext

# Create your models here.

class StudentClass(models.Model):
    student_class = models.CharField(max_length=100)
    class_summary = models.CharField(max_length=500)
    # Image/Media to be added later
    class_slug = models.SlugField(max_length=100)

    class Meta:
        verbose_name_plural = "Classes"

    def validate_unique(self, *args, **kwargs):
        self.class_slug = slugify(self.student_class)
        super(StudentClass, self).validate_unique(*args, **kwargs)
        if self.__class__.objects.filter(class_slug=self.class_slug).exists():
            raise ValidationError(message=f"Class with name \"{self.student_class}\" already exists.",
                                  code='unique_together',)

    def __str__(self):
        return self.student_class

class StudentSubject(models.Model):
    student_subject = models.CharField(max_length=100)
    subject_summary = models.CharField(max_length=500)
    # Image/Media to be added later
    subject_slug = models.SlugField(max_length=100)

    student_class = models.ForeignKey(StudentClass, default=1, verbose_name="Class", on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name_plural = "Subjects"

    def validate_unique(self, *args, **kwargs):
        self.subject_slug = slugify(self.student_subject)
        super(StudentSubject, self).validate_unique(*args, **kwargs)
        if self.__class__.objects.filter(subject_slug=self.subject_slug, student_class__class_slug=self.student_class.class_slug).exists():
            raise ValidationError(message=f"Subject with name \"{self.student_subject}\" already exists.",
                                  code='unique_together',)

    def __str__(self):
        return self.student_subject

class StudentChapter(models.Model):
    student_chapter = models.CharField(max_length=100)
    chapter_summary = models.CharField(max_length=500)
    # Image/Media to be added later
    chapter_slug = models.SlugField(max_length=100)

    student_subject = models.ForeignKey(StudentSubject, default=1, verbose_name="Subject", on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name_plural = "Chapters"

    def validate_unique(self, *args, **kwargs):
        self.chapter_slug = slugify(self.student_chapter)
        super(StudentChapter, self).validate_unique(*args, **kwargs)
        if self.__class__.objects.filter(chapter_slug=self.chapter_slug, student_subject__subject_slug=self.student_subject.subject_slug, student_subject__student_class__class_slug=self.student_subject.student_class.class_slug).exists():
            raise ValidationError(message=f"Chapter with name \"{self.student_chapter}\" already exists.",
                                  code='unique_together',)

    def __str__(self):
        return self.student_chapter

class StudentSection(models.Model):
    def user_directory_path(instance, filename):
        return f"{instance.section_video_base}{instance.section_slug}.{filename.split('.')[-1]}"

    student_section = models.CharField(max_length=100)
    section_summary = models.CharField(max_length=500)
    section_slug = models.SlugField(max_length=100)

    section_video = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    section_video_base = models.CharField(max_length=300)
    section_text = models.TextField()

    student_chapter = models.ForeignKey(StudentChapter, default=1, verbose_name="Chapter", on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name_plural = "Sections"

    def validate_unique(self, *args, **kwargs):
        self.section_slug = slugify(self.student_section)
        super(StudentSection, self).validate_unique(*args, **kwargs)
        if self.__class__.objects.filter(section_slug=self.section_slug, student_chapter__chapter_slug=self.student_chapter.chapter_slug, student_chapter__student_subject__subject_slug=self.student_chapter.student_subject.subject_slug, student_chapter__student_subject__student_class__class_slug=self.student_chapter.student_subject.student_class.class_slug).exists():
            raise ValidationError(message=f"Section with name \"{self.student_section}\" already exists.",
                                  code='unique_together',)

    def delete(self, *args, **kwargs):
        if self.section_video:
            self.section_video.storage.delete(self.section_video.name)
        super(StudentSection, self).delete(*args, **kwargs)

    def __str__(self):
        return self.student_section

class StudentCategory(models.Model):
    def user_directory_path(instance, filename):
        return f"student/content/{slugify(instance.category_slug)}/{instance.category_slug}.{filename.split('.')[-1]}"

    student_category = models.CharField(max_length=100)
    category_summary = models.CharField(max_length=500)
    category_slug = models.SlugField(max_length=100)

    category_image = models.FileField(upload_to=user_directory_path)

    class Meta:
        verbose_name_plural = "Categories"

    def validate_unique(self, *args, **kwargs):
        self.category_slug = slugify(self.student_category)
        super(StudentCategory, self).validate_unique(*args, **kwargs)
        if self.__class__.objects.filter(category_slug=self.category_slug).exists():
            raise ValidationError(message=f"Category with name \"{self.student_category}\" already exists.",
                                  code='unique_together',)

    def delete(self, *args, **kwargs):
        if self.category_image:
            self.category_image.storage.delete(self.category_image.name)
        super(StudentCategory, self).delete(*args, **kwargs)

    def __str__(self):
        return self.student_category

class StudentContent(models.Model):
    def user_directory_path(instance, filename):
        return f"student/content/{instance.content_category.category_slug}/{slugify(instance.student_content)}.{filename.split('.')[-1]}"

    student_content = models.CharField(max_length=100)
    content_text = models.TextField()
    content_time = models.DateTimeField(auto_now_add=True)
    content_file = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    content_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="User", on_delete=models.CASCADE)
    content_category = models.ForeignKey(StudentCategory, verbose_name="Category", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Content"

    def file_type(self):
        name, extension = splitext(self.content_file.name.lower())
        if extension in ['.apng', '.avif', '.gif', '.jpg', '.jpeg', '.jfif', '.pjpeg', '.pjp', '.png', '.svg', '.webp']:
            return 'image'
        elif extension in ['.mp4', 'webm']:
            return 'video'
        elif extension in ['.mp3', '.wav', '.ogg', '.m4a']:
            return 'audio'
        else:
            return 'file'

    def delete(self, *args, **kwargs):
        if self.content_file:
            self.content_file.storage.delete(self.content_file.name)
        super(StudentContent, self).delete(*args, **kwargs)

    def __str__(self):
        return self.student_content

class UploadImage(models.Model):
    def user_directory_path(instance, filename):
        return f"upload/images/{slugify(instance.image_name)}.{filename.split('.')[-1]}"

    image_name = models.CharField(max_length=100)
    image_summary = models.CharField(max_length=500)

    image_file = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Images"

    def delete(self, *args, **kwargs):
        if self.image_file:
            self.image_file.storage.delete(self.image_file.name)
        super(UploadImage, self).delete(*args, **kwargs)

    def __str__(self):
        return self.image_name

class UploadVideo(models.Model):
    def user_directory_path(instance, filename):
        return f"upload/videos/{slugify(instance.video_name)}.{filename.split('.')[-1]}"

    video_name = models.CharField(max_length=100)
    video_summary = models.CharField(max_length=500)

    video_file = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Videos"

    def delete(self, *args, **kwargs):
        if self.video_file:
            self.video_file.storage.delete(self.video_file.name)
        super(UploadVideo, self).delete(*args, **kwargs)

    def __str__(self):
        return self.video_name

class UploadAudio(models.Model):
    def user_directory_path(instance, filename):
        return f"upload/audios/{slugify(instance.audio_name)}.{filename.split('.')[-1]}"

    audio_name = models.CharField(max_length=100)
    audio_summary = models.CharField(max_length=500)

    audio_file = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Audios"

    def delete(self, *args, **kwargs):
        if self.audio_file:
            self.audio_file.storage.delete(self.audio_file.name)
        super(UploadAudio, self).delete(*args, **kwargs)

    def __str__(self):
        return self.audio_name

class UploadFile(models.Model):
    def user_directory_path(instance, filename):
        return f"upload/files/{slugify(instance.file_name)}.{filename.split('.')[-1]}"

    file_name = models.CharField(max_length=100)
    file_summary = models.CharField(max_length=500)

    file_file = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Files"

    def delete(self, *args, **kwargs):
        if self.file_file:
            self.file_file.storage.delete(self.file_file.name)
        super(UploadFile, self).delete(*args, **kwargs)

    def __str__(self):
        return self.file_name

class UploadFeed(models.Model):
    def user_directory_path(instance, filename):
        return f"feed/{instance.feed_user}/{filename}"

    feed_text = models.CharField(max_length=5000)
    feed_date = models.DateTimeField(auto_now_add=True)
    feed_file = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    feed_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="User", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Feed"

    def file_type(self):
        name, extension = splitext(self.feed_file.name.lower())
        if extension in ['.apng', '.avif', '.gif', '.jpg', '.jpeg', '.jfif', '.pjpeg', '.pjp', '.png', '.svg', '.webp']:
            return 'image'
        elif extension in ['.mp4', 'webm']:
            return 'video'
        elif extension in ['.mp3', '.wav', '.ogg', '.m4a']:
            return 'audio'
        else:
            return 'file'

    def delete(self, *args, **kwargs):
        if self.feed_file:
            self.feed_file.storage.delete(self.feed_file.name)
        super(UploadFeed, self).delete(*args, **kwargs)

    def __str__(self):
        return self.feed_text[:15]+"..."

class Chat(models.Model):
    chat_recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Chat Recipients", related_name="chats")
    last_message_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Last Message Sender", on_delete=models.CASCADE)
    last_message_text = models.CharField(max_length=500)
    last_message_time = models.DateTimeField(auto_now=True)
    last_message_seen = models.BooleanField()

    def __str__(self):
        return ", ".join([x.username for x in self.chat_recipients.all()])

class Message(models.Model):
    message_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Message Sender", on_delete=models.CASCADE)
    message_text = models.CharField(max_length=500)
    message_time = models.DateTimeField(auto_now_add=True)
    message_chat = models.ForeignKey(Chat, verbose_name="Chat", on_delete=models.CASCADE)

    def __str__(self):
        return ", ".join([x.username for x in self.message_chat.chat_recipients.all()]) + ": " + self.message_text[:15]+"..."

class Notification(models.Model):
    def user_directory_path(instance, filename):
        return f"notifications/{filename}"

    notif_title = models.CharField(max_length=500)
    notif_text = models.CharField(max_length=5000)
    notif_time = models.DateTimeField(auto_now_add=True)
    notif_file = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    def delete(self, *args, **kwargs):
        if self.notif_file:
            self.notif_file.storage.delete(self.notif_file.name)
        super(Notification, self).delete(*args, **kwargs)

    def __str__(self):
        return self.notif_title
