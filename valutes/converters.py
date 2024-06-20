from django.urls import converters
from django.urls import register_converter

class YearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value


class ColorConverter(converters.StringConverter):
    regex = '[a-fA-F0-9]{6}'

    def to_python(self, value):
        return '#' + value

    def to_url(self, value):
        return value[1:]
