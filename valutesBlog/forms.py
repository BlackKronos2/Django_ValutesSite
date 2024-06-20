from django import forms
from .models import *
from django.core.validators import *


def MarksValidator(value):
    exclamation_count = value.count('!')
    question_count = value.count('?')

    if exclamation_count >= 3 or question_count >= 3:
        raise ValidationError("Большое количество восклицательных и вопросительных знаков.")


def TitleCharsValidator(value):
    pattern = re.compile(r'[+=<>{}[\]~`@#$%^&*_\-|\\/\'"\s]')

    if pattern.search(value):
        raise ValidationError("Заголовок содержит недопустимые символы.")

class AddCurrencyArticleForm(forms.ModelForm):

    currencies = forms.ModelMultipleChoiceField(
        queryset=Currency.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label="Валюты"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['article_order'].empty_label = 'Без статуса'
        self.fields['article_order'].required = False
        self.fields['title'].validators = [MarksValidator]

    class Meta:
        model = CurrencyArticle
        fields = ['title', 'full_text', 'photo', 'article_order', 'currencies', 'display_status', 'slug', 'date']

class EditCurrencyArticleForm(forms.ModelForm):

    currencies = forms.ModelMultipleChoiceField(
        queryset=Currency.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label="Валюты"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['article_order'].empty_label = 'Без статуса'
        self.fields['article_order'].required = False
        self.fields['title'].validators = [MarksValidator]

    class Meta:
        model = CurrencyArticle
        fields = ['title', 'full_text', 'photo', 'article_order', 'currencies', 'display_status', 'slug', 'date']

class DeleteCurrencyArticleForm(forms.ModelForm):
    class Meta:
        model = CurrencyArticle
        fields = []