# Generated by Django 5.0.4 on 2024-04-24 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_order_order_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_size',
            field=models.CharField(choices=[('большой заказ', 'большой заказ'), ('маленький заказ', 'маленький заказ')], default='большой заказ', max_length=30, verbose_name='Размер заказа'),
        ),
    ]
