# Generated by Django 5.0.2 on 2024-05-19 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valutes', '0004_alter_currency_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currency',
            options={'verbose_name': 'Валюта', 'verbose_name_plural': 'Валюты'},
        ),
        migrations.AlterField(
            model_name='currency',
            name='num_code',
            field=models.CharField(max_length=10, verbose_name='Код числовой'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='parse_code',
            field=models.CharField(max_length=10, verbose_name='Код ЦБ'),
        ),
    ]
