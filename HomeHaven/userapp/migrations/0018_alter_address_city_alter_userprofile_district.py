# Generated by Django 4.1.7 on 2023-03-14 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0017_remove_review_img_alter_address_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Hydrabad', 'Hydrabad'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Coimbator', 'Coimbator'), ('Kannur', 'Kannur'), ('Kozhikkode', 'Kozhikkode'), ('Madurai', 'Madurai'), ('Banglore', 'Banglore'), ('Hubli', 'Hubli'), ('Ernakulam', 'Ernakulam')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Hydrabad', 'Hydrabad'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Coimbator', 'Coimbator'), ('Kannur', 'Kannur'), ('Kozhikkode', 'Kozhikkode'), ('Madurai', 'Madurai'), ('Banglore', 'Banglore'), ('Hubli', 'Hubli'), ('Ernakulam', 'Ernakulam')], max_length=20, null=True),
        ),
    ]