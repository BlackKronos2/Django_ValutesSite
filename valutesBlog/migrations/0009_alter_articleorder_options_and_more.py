# Generated by Django 5.0.2 on 2024-05-19 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valutesBlog', '0008_remove_currencyarticle_anons'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articleorder',
            options={'verbose_name': 'Тег новостей', 'verbose_name_plural': 'Теги новостей'},
        ),
        migrations.AlterModelOptions(
            name='currencyarticle',
            options={'verbose_name': 'Новость', 'verbose_name_plural': 'Новости'},
        ),
        migrations.AddField(
            model_name='currencyarticle',
            name='photo',
            field=models.ImageField(null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='currencyarticle',
            name='display_status',
            field=models.CharField(choices=[('CD', 'Можно отобразить'), ('NCD', 'Нельзя отобразить')], default='CD', max_length=3, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='currencyarticle',
            name='full_text',
            field=models.TextField(verbose_name='Полный текст'),
        ),
        migrations.AlterField(
            model_name='currencyarticle',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рейтинг'),
        ),
    ]