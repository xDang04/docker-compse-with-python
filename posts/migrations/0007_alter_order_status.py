# Generated by Django 4.1 on 2024-11-04 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Chờ xác nhận', 'Chờ xác nhận'), ('Chờ giao hàng', 'Chờ giao hàng'), ('Đang giao hàng', 'Đang giao hàng'), ('Đã nhận hàng', 'Đã nhận hàng'), ('Đã hủy', 'Đã hủy')], max_length=50),
        ),
    ]