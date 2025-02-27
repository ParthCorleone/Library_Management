# Generated by Django 5.1.6 on 2025-02-25 16:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarymg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookIssuance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issued_date', models.DateTimeField(auto_now_add=True)),
                ('returned_date', models.DateTimeField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='librarymg.book')),
                ('issued_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
