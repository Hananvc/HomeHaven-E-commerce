# Generated by Django 4.1.7 on 2023-03-03 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0003_productimage_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='name',
        ),
    ]