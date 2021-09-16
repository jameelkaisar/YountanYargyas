from django.db import models
from datetime import datetime

# Create your models here.

class Book(models.Model):
    book_title = models.CharField(max_length=100)
    book_description = models.TextField()
    book_published = models.DateTimeField("When was this book published?", default=datetime.now())

    def __str__(self):
        return self.book_title
