# Generated by Django 3.1.4 on 2021-01-04 09:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20210104_0256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bbuser',
            name='phone',
            field=models.CharField(blank=True, error_messages={'unique': 'A user with that phone number already exists.'}, max_length=14, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9(999)9999999'", regex='^\\+\\d\\(\\d{3}\\)\\d{7}$')], verbose_name='phone number'),
        ),
    ]
