# Generated by Django 4.1 on 2024-11-20 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_payment_vnpay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment_vnpay',
            name='order_id',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
    ]
