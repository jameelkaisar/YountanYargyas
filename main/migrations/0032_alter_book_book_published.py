# Generated by Django 3.2.7 on 2021-09-19 11:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_alter_book_book_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_published',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 19, 17, 23, 41, 19567), verbose_name='When was this book published?'),
        ),
    ]
