# Generated by Django 3.0.8 on 2020-07-31 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MoneySource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_level_source', models.CharField(help_text='Source-first-level', max_length=200)),
                ('second_level_source', models.CharField(blank=True, help_text='Source-second-level', max_length=200)),
            ],
            options={
                'ordering': ['-first_level_source'],
            },
        ),
        migrations.CreateModel(
            name='SpendingKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_level_kind', models.CharField(help_text='Kind-first-level', max_length=200)),
                ('second_level_kind', models.CharField(blank=True, help_text='Kind-second-level', max_length=200)),
            ],
            options={
                'ordering': ['-first_level_kind'],
            },
        ),
        migrations.CreateModel(
            name='Spendings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_field', models.DateField(default='2020-07-31')),
                ('ammount', models.FloatField(help_text='000.00')),
                ('comment', models.TextField(blank=True, help_text='Any comments?')),
                ('kind', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='money_move.SpendingKind')),
            ],
            options={
                'ordering': ['-date_field'],
            },
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_field', models.DateField(default='2020-07-31')),
                ('ammount', models.FloatField(help_text='000.00')),
                ('comment', models.TextField(blank=True, help_text='Any comments?')),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='money_move.MoneySource')),
            ],
            options={
                'ordering': ['-date_field'],
            },
        ),
    ]
