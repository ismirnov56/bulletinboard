# Generated by Django 3.1.4 on 2021-02-05 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import src.announcement.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('announcement', '0005_auto_20210131_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcements',
            name='title',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='announcements',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(upload_to=src.announcement.models.announcements_directory_path, validators=[src.announcement.models.validate_image]),
        ),
    ]
