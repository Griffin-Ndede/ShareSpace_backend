# Generated by Django 5.1.4 on 2025-04-18 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Resources', '0005_rename_categories_category_rename_faqs_faq_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
