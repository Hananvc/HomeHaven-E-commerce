# Generated by Django 4.1.7 on 2023-03-13 06:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userapp', '0008_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Hydrabad', 'Hydrabad'), ('Hubli', 'Hubli'), ('Coimbator', 'Coimbator'), ('Kannur', 'Kannur'), ('Kozhikkode', 'Kozhikkode'), ('Ernakulam', 'Ernakulam'), ('Madurai', 'Madurai'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Banglore', 'Banglore')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Hydrabad', 'Hydrabad'), ('Hubli', 'Hubli'), ('Coimbator', 'Coimbator'), ('Kannur', 'Kannur'), ('Kozhikkode', 'Kozhikkode'), ('Ernakulam', 'Ernakulam'), ('Madurai', 'Madurai'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Banglore', 'Banglore')], max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField(blank=True, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userapp.product')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
