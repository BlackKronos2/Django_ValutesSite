from django.contrib import admin
from .models import Currency

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'сurrency_name', 'char_code', 'num_code')
    list_display_links = ('id', 'char_code')

# Register your models here.
admin.site.register(Currency, CurrencyAdmin)
