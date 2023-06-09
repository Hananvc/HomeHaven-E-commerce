# Generated by Django 4.1.7 on 2023-03-13 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0010_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Kozhikkode', 'Kozhikkode'), ('Kannur', 'Kannur'), ('Madurai', 'Madurai'), ('Coimbator', 'Coimbator'), ('Banglore', 'Banglore'), ('Ernakulam', 'Ernakulam'), ('Hydrabad', 'Hydrabad'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Hubli', 'Hubli')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Kozhikkode', 'Kozhikkode'), ('Kannur', 'Kannur'), ('Madurai', 'Madurai'), ('Coimbator', 'Coimbator'), ('Banglore', 'Banglore'), ('Ernakulam', 'Ernakulam'), ('Hydrabad', 'Hydrabad'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Hubli', 'Hubli')], max_length=20, null=True),
        ),
    ]
