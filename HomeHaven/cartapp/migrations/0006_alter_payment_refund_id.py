# Generated by Django 4.1.7 on 2023-03-31 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0005_alter_payment_payment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='refund_id',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
