# Generated by Django 5.1.6 on 2025-02-27 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarymg', '0008_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
