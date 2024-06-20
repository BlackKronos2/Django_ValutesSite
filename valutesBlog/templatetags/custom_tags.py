from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='custom_date_format')
def custom_date_format(value):
    value = value.replace(' ', '')  # Удаляем все пробелы из значения
    parsed_date = "-".join(value.split('-')[:2])  # Удаляем последний символ из дня и объединяем обратно
    formatted_date = datetime.strptime(parsed_date, '%Y-%m').strftime('%d.%m.%Y')
    return formatted_date

@register.filter
def get_range(value):
    return range(value)