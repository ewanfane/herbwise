# Generated by Django 5.1.5 on 2025-02-19 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_info_record_data'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Box',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]
