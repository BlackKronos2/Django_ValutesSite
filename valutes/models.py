from django.db import models
from django.utils.text import slugify

class CurrencyManager(models.Manager):
    def get_currencies(self):
        return self.all()

class Currency(models.Model):
    parse_code = models.CharField(max_length=10, verbose_name='Код ЦБ')
    num_code = models.CharField(max_length=10, verbose_name='Код числовой')

    char_code = models.CharField(max_length=10, verbose_name='Код валюты')
    nominal = models.IntegerField(default=1, verbose_name='Номинал')

    сurrency_name = models.CharField(max_length=20, verbose_name='Название')

    slug = models.SlugField(unique=False,db_index=True, verbose_name="URL")
    objects = CurrencyManager()

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    def save(self, *args, **kwargs):
        if not self.slug: # Генерируем слаг только если он отсутствует
            self.slug = slugify(self.char_code)
        super(Currency, self).save(*args, **kwargs)

    def __str__(self):
        return self.сurrency_name
