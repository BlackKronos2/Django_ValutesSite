from django.urls import path
from . import views

app_name = "valutesBlog"

urlpatterns = [
    path('', views.MainPageView.as_view(), name='blog_index'),
    path('order/<int:order_id>/', views.BlogWithOrderView.as_view(), name='blog_with_order'),
    path('order/lates/', views.BlogLatesView.as_view(), name='blog_lates'),
    path('order/earliest/', views.BlogEarliestView.as_view(), name='blog_earliest'),
    path('order/sort_rating/', views.BlogSortRatingView.as_view(), name='blog_sort_rating'),
    path('post/<slug:post_slug>/', views.ShowArticleView.as_view(), name='post'),
    path('add_article/', views.AddArticleView.as_view(), name='add_article'),
    path('edit/<slug:post_slug>/', views.EditCurrencyArticleView.as_view(), name='edit_article'),
    path('delete/<slug:post_slug>/', views.DeleteCurrencyArticleView.as_view(), name='delete_article'),
]