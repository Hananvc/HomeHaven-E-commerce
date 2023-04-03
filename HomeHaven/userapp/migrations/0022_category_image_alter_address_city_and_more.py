# Generated by Django 4.1.7 on 2023-03-30 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0021_address_default_alter_address_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category_images/'),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Madurai', 'Madurai'), ('Hubli', 'Hubli'), ('Coimbator', 'Coimbator'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Hydrabad', 'Hydrabad'), ('Banglore', 'Banglore'), ('Kozhikkode', 'Kozhikkode'), ('Kannur', 'Kannur'), ('Ernakulam', 'Ernakulam')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Madurai', 'Madurai'), ('Hubli', 'Hubli'), ('Coimbator', 'Coimbator'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Hydrabad', 'Hydrabad'), ('Banglore', 'Banglore'), ('Kozhikkode', 'Kozhikkode'), ('Kannur', 'Kannur'), ('Ernakulam', 'Ernakulam')], max_length=20, null=True),
        ),
    ]
