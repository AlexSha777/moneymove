# Generated by Django 3.0.8 on 2020-11-13 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money_move', '0006_auto_20201023_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cash',
            name='date_field',
            field=models.DateField(default='2020-11-13'),
        ),
        migrations.AlterField(
            model_name='income',
            name='date_field',
            field=models.DateField(default='2020-11-13'),
        ),
        migrations.AlterField(
            model_name='spendings',
            name='date_field',
            field=models.DateField(default='2020-11-13'),
        ),
    ]