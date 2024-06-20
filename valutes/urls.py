from django.urls import path, register_converter, include
from . import views, converters
from django.http import HttpResponseNotFound
from .views import *

register_converter(converters.YearConverter, 'year')

urlpatterns = [
    path('', views.page_from_name, {'file_name': 'index'}, name='index'),
    path('valute/<slug:slug>/', ValuteView.as_view(), name='currency_detail_view'),
    path('about_site/', views.page_from_name, {'file_name': 'about_site'}, name='about'),
    path('about_company/', views.page_from_name, {'file_name': 'about_company'}, name='about_site'),
    path('faq/', views.page_from_name, {'file_name': 'FAQ'}, name='FAQ'),

    path('404/', lambda request: HttpResponseNotFound('Страница не найдена - Ошибка адреса')),

    path('valutes/convert_currency/', views.convert_currency, name='convert_currency'),

    path('current-exchange-rate/<str:valute_code>/', CurrentExchangeRateView.as_view(), name='current_exchange_rate'),
    path('currency-chart/<str:valute_code>/', views.get_currency_rates, name='currency_chart'),
]