import requests
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.generic import View
from valutes.models import Currency
from valutesBlog.models import ArticleOrder

from valutesParser.valutesParsers import ValutesParser

class CurrencyArticleMixin:
    def get_mixin_context(self, context):
        currencies = Currency.objects.get_currencies()

        half_size = len(currencies) // 2
        currencies_first_half = currencies[:half_size]
        currencies_second_half = currencies[half_size:]

        context['article_orders'] = ArticleOrder.displayable_objects.get_article_orders_with_article_count()
        context['currencies'] = currencies
        context['currencies_first_half'] = currencies_first_half
        context['currencies_second_half'] = currencies_second_half
        return context

def page_from_name(request, file_name):
    currencies = Currency.objects.get_currencies()
    middle_index = (len(currencies) + 1) // 2
    currencies_first_half = currencies[:middle_index]
    currencies_second_half = currencies[middle_index:]

    return render(request, file_name + '.html', {'currencies': currencies, 'currencies_first_half': currencies_first_half, 'currencies_second_half': currencies_second_half})


def custom_404(request, exception):
    return redirect('404.html')


class ValuteView(CurrencyArticleMixin, TemplateView):
    template_name = 'valute.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        currency = get_object_or_404(Currency, slug=kwargs['slug'])
        currencies = Currency.objects.get_currencies()
        rates = ValutesParser().parse_currencies()

        rate = [valute for valute in rates if valute.char_code == currency.char_code][0].value
        rates = [v for v in rates if any(v.char_code == c.char_code for c in currencies)]

        for valute in rates:
            new_value = (1 / rate) * valute.value
            valute.value = new_value

        context['valute'] = currency
        context['value'] = rate
        context['currencies'] = currencies
        context['rates'] = rates

        return self.get_mixin_context(context)

def get_exchange_rate(request):
    currencies = Currency.objects.get_currencies
    return render(request, 'exchange_rate_form.html', {'currencies': currencies})

@require_GET  # Указываем, что представление должно обрабатывать только GET-запросы
def convert_currency(request):
    value = float(request.GET.get('value', 0))
    multiplier = float(request.GET.get('multiplier', 1))
    calculated_value = round(value * multiplier, 2)
    return JsonResponse({'calculated_value': calculated_value})


class CurrentExchangeRateView(CurrencyArticleMixin, View):
    def get(self, request, valute_code):
        currencies = Currency.objects.get_currencies()
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        data = response.json()
        rate = data['Valute'][valute_code]['Value']

        half_size = len(currencies) // 2
        currencies_first_half = currencies[:half_size]
        currencies_second_half = currencies[half_size:]

        context = {'rate': rate, 'valute_code': valute_code, 'currencies': currencies}
        context['article_orders'] = ArticleOrder.displayable_objects.get_article_orders_with_article_count()
        context['currencies'] = currencies
        context['currencies_first_half'] = currencies_first_half
        context['currencies_second_half'] = currencies_second_half

        return render(request, 'current_exchange_rate.html', context)


def get_currency_rates(request, valute_code):
    dates, rates = ValutesParser().get_currency_history(valute_code)
    currencies = Currency.objects.get_currencies

    for i in range(0, len(rates)):
        cr_data = {'date': dates[i], 'value': rates[i]}
        rates.append(cr_data)

    return render(request, 'currency_chart.html', {'rates': rates, 'dates' : dates, 'currencies' : currencies})

