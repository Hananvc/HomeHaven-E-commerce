# Generated by Django 4.1.7 on 2023-03-13 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0012_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Thiruvananthapuram', 'Thiruvananthapuram'), ('Madurai', 'Madurai'), ('Coimbator', 'Coimbator'), ('Kannur', 'Kannur'), ('Hubli', 'Hubli'), ('Hydrabad', 'Hydrabad'), ('Ernakulam', 'Ernakulam'), ('Banglore', 'Banglore'), ('Kozhikkode', 'Kozhikkode')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Thiruvananthapuram', 'Thiruvananthapuram'), ('Madurai', 'Madurai'), ('Coimbator', 'Coimbator'), ('Kannur', 'Kannur'), ('Hubli', 'Hubli'), ('Hydrabad', 'Hydrabad'), ('Ernakulam', 'Ernakulam'), ('Banglore', 'Banglore'), ('Kozhikkode', 'Kozhikkode')], max_length=20, null=True),
        ),
    ]
