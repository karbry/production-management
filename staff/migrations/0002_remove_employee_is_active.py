# Generated by Django 3.2.9 on 2021-11-25 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='is_active',
        ),
    ]
