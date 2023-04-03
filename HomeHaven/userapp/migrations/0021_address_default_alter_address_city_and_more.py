# Generated by Django 4.1.7 on 2023-03-27 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0020_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='default',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Kannur', 'Kannur'), ('Hubli', 'Hubli'), ('Madurai', 'Madurai'), ('Hydrabad', 'Hydrabad'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Banglore', 'Banglore'), ('Kozhikkode', 'Kozhikkode'), ('Coimbator', 'Coimbator'), ('Ernakulam', 'Ernakulam')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Kannur', 'Kannur'), ('Hubli', 'Hubli'), ('Madurai', 'Madurai'), ('Hydrabad', 'Hydrabad'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Banglore', 'Banglore'), ('Kozhikkode', 'Kozhikkode'), ('Coimbator', 'Coimbator'), ('Ernakulam', 'Ernakulam')], max_length=20, null=True),
        ),
    ]
