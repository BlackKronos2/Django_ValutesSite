from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

class ArticlesFilter(admin.SimpleListFilter):
    title = 'Связь с валютами'
    parameter_name = 'has_currencies'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Со связанными валютами'),
            ('no', 'Без связанных валют'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.annotate(num_currencies=Count('currencies')).filter(num_currencies__gt=0)
        elif self.value() == 'no':
            return queryset.annotate(num_currencies=Count('currencies')).filter(num_currencies=0)

@admin.register(CurrencyArticle)
class ArticlesAdmin(admin.ModelAdmin):
    fields = ['title', 'photo', 'photo_preview', 'full_text', 'date','rating', 'display_status','article_length', 'article_order', 'currencies']
    filter_horizontal = ['currencies']
    readonly_fields = ['display_status','article_length', 'photo_preview']
    list_display = ('id', 'title', 'article_length','rating', 'date', 'display_status', 'article_order')
    list_display_links = ('id', 'title')
    ordering = ['-date', 'title']
    list_editable = ('display_status', 'article_order')
    list_per_page = 3
    actions = ['article_publish', 'article_hide']
    search_fields = ['title']
    list_filter = [ArticlesFilter, 'article_order', 'display_status']

    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100" height="100">')
        else:
            return '(Нет фото)'

    photo_preview.short_description = 'Фото на новости'

    @admin.display(description='Размер')
    def article_length(self, article: CurrencyArticle):
        return f'{len(article.full_text)} символов'

    @admin.action(description='Отобразить')
    def article_publish(self, request, queryset):
        count = queryset.update(display_status=DisplayStatus.CAN_DISPLAY)
        self.message_user(request, f'Изменено {count} записей')

    @admin.action(description='Скрыть')
    def article_hide(self, request, queryset):
        count = queryset.update(display_status=DisplayStatus.CANNOT_DISPLAY)
        self.message_user(request, f'Изменено {count} записей')

# Register your models here.
admin.site.register(ArticleOrder)