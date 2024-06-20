from django.urls import path, register_converter, include
from django.http import HttpResponseNotFound
from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('valutes/', include('valutes.urls')),
    path('blog/', include('valutesBlog.urls')),
    path('system/', include('system_pages.urls')),
    path('', RedirectView.as_view(url='valutes/', permanent=True)),
    path('', include('valutesBlog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Панель управления"
admin.site.index_title = "Сайт обзора валют"
