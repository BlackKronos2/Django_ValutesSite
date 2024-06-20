import os
from django.utils import timezone

from django.db import models
from valutes.models import Currency
from django.db.models import Value
from django.db.models import Count
from django.db.models import F
from django.urls import reverse
from django.db.models.functions import Concat, Substr

class DisplayStatus(models.TextChoices):
    CAN_DISPLAY = 'CD', 'Можно отобразить'
    CANNOT_DISPLAY = 'NCD', 'Нельзя отобразить'

class ArticleOrderManager(models.Manager):
    def get_article_orders(self):
        return self.filter(display_status=DisplayStatus.CAN_DISPLAY)

    def get_article_orders_with_article_count(self):
        # Получаем базовый queryset
        queryset = super().get_queryset()
        # Аннотируем количество связанных объектов CurrencyArticle
        queryset = queryset.annotate(articles_count=Count('articles'))
        return queryset

class ArticleOrder(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название')
    displayable_objects = ArticleOrderManager()

    class Meta:
        verbose_name = 'Тег новостей'
        verbose_name_plural = 'Теги новостей'

    def __str__(self):
        return self.title

class CurrencyArticleManager(models.Manager):
    def get_displayable_articles(self):
        return self.annotate(is_active=Value(DisplayStatus.CAN_DISPLAY, output_field=models.CharField())).filter(display_status=DisplayStatus.CAN_DISPLAY)

    def get_articles_by_order_id(self, order_id):
        return self.filter(article_order_id=order_id)

    def get_articles_lates(self):
        return self.order_by('-date')

    def get_articles_earliest(self):
        return self.order_by('date')

    def get_articles_sort_rating(self):
        return self.order_by(F('rating'))




def generate_photo_filename(instance, filename):
    """
    Генерация случайного имени файла для фотографии.
    """
    _, ext = os.path.splitext(filename)
    current_datetime = timezone.now()
    new_filename = f"{current_datetime.strftime('%Y%m%d%H%M%S')}{instance.pk}{ext}"
    return os.path.join("photos", current_datetime.strftime("%Y/%m/%d"), new_filename)

class CurrencyArticle(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    full_text = models.TextField(verbose_name='Полный текст')
    date = models.DateField(verbose_name='Дата публикации')
    display_status = models.CharField(max_length=3, choices=DisplayStatus.choices, default=DisplayStatus.CAN_DISPLAY
                                      ,verbose_name='Статус')

    photo = models.ImageField(upload_to=generate_photo_filename, verbose_name="Фото", null=True)

    article_order = models.ForeignKey(ArticleOrder, on_delete=models.SET_NULL, verbose_name='Тип новости', related_name='articles', null=True)
    currencies = models.ManyToManyField(Currency, verbose_name='Валюты')

    objects = models.Manager()
    displayable_objects = CurrencyArticleManager()

    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", null=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    @property
    def anons(self):
        # Получаем анонс из первых 250 символов full_text и добавляем троеточие в конце
        return self.full_text[:250] + '...' \
            if len(self.full_text) > 250 \
            else self.full_text

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.title

