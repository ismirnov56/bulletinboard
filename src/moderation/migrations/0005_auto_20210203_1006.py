# Generated by Django 3.1.4 on 2021-02-03 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0005_auto_20210131_1742'),
        ('moderation', '0004_auto_20210201_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderation',
            name='announcement',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='announcement.announcements'),
        ),
    ]
