# Generated by Django 5.0.4 on 2024-04-24 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_order_order_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cell',
            name='free_place',
            field=models.FloatField(default=1, verbose_name='Свободное место'),
        ),
    ]
