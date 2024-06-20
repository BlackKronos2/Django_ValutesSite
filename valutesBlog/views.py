from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import HttpResponse
from valutes.models import Currency
from valutesBlog.models import CurrencyArticle
from valutesBlog.models import ArticleOrder
from .forms import *
from valutesBlog.models import CurrencyArticleManager
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, TemplateView, View, FormView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.

class CurrencyArticleMixin:
    def get_mixin_context(self, context):
        context['article_orders'] = ArticleOrder.displayable_objects.get_article_orders_with_article_count()
        currencies = Currency.objects.get_currencies()

        half_size = len(currencies) // 2
        currencies_first_half = currencies[:half_size]
        currencies_second_half = currencies[half_size:]

        context['article_orders'] = ArticleOrder.displayable_objects.get_article_orders_with_article_count()
        context['currencies'] = currencies
        context['currencies_first_half'] = currencies_first_half
        context['currencies_second_half'] = currencies_second_half
        return context

class MainPageView(CurrencyArticleMixin, ListView):
    paginate_by = 2

    model = CurrencyArticle
    template_name = 'blog_index.html'
    context_object_name = 'displayable_articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

class BlogWithOrderView(CurrencyArticleMixin, ListView):
    paginate_by = 2

    model = CurrencyArticle
    template_name = 'blog_index.html'
    context_object_name = 'displayable_articles'

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return CurrencyArticle.displayable_objects.get_articles_by_order_id(order_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_id'] = self.kwargs['order_id']
        return self.get_mixin_context(context)


class BlogLatesView(CurrencyArticleMixin, ListView):
    paginate_by = 2

    model = CurrencyArticle
    template_name = 'blog_index.html'
    context_object_name = 'displayable_articles'

    def get_queryset(self):
        return CurrencyArticle.displayable_objects.get_articles_lates()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

class BlogEarliestView(CurrencyArticleMixin, ListView):
    paginate_by = 2

    model = CurrencyArticle
    template_name = 'blog_index.html'
    context_object_name = 'displayable_articles'

    def get_queryset(self):
        return CurrencyArticle.displayable_objects.get_articles_earliest()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

class BlogSortRatingView(CurrencyArticleMixin, ListView):
    paginate_by = 2

    model = CurrencyArticle
    template_name = 'blog_index.html'
    context_object_name = 'displayable_articles'

    def get_queryset(self):
        return CurrencyArticle.displayable_objects.get_articles_sort_rating()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class ShowArticleView(CurrencyArticleMixin, DetailView):
    model = CurrencyArticle
    template_name = 'article_show.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['post'] = self.object
        return self.get_mixin_context(context)

class AddArticleView(PermissionRequiredMixin, CurrencyArticleMixin, CreateView):
    model = CurrencyArticle
    form_class = AddCurrencyArticleForm
    template_name = 'add_article.html'
    success_url = reverse_lazy('valutesBlog:blog_index')
    permission_required = 'valutesBlog.add_currencyarticle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['displayable_articles'] = CurrencyArticle.displayable_objects.all()
        return self.get_mixin_context(context)

class EditCurrencyArticleView(PermissionRequiredMixin, CurrencyArticleMixin, UpdateView):
    model = CurrencyArticle
    fields = ['title', 'full_text', 'photo', 'article_order', 'display_status', 'date']
    slug_url_kwarg = 'post_slug'
    template_name = 'edit_article.html'
    success_url = reverse_lazy('valutesBlog:blog_index')
    permission_required = 'valutesBlog.change_currencyarticle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

class DeleteCurrencyArticleView(CurrencyArticleMixin, DeleteView):
    model = CurrencyArticle
    template_name = 'delete_article.html'
    slug_url_kwarg = 'post_slug'
    success_url = reverse_lazy('currency_article_list')

    def get_object(self):
        _slug = self.kwargs.get('post_slug')
        return get_object_or_404(CurrencyArticle, slug=_slug)

    def get_success_url(self):
        return reverse('valutesBlog:blog_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

