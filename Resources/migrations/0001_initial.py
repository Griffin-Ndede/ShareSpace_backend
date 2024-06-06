# Generated by Django 5.0.6 on 2024-06-06 07:15

import Resources.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('image_url', models.ImageField(blank=True, null=True, upload_to=Resources.models.upload_to)),
            ],
        ),
    ]