from importlib import import_module

from django.conf.urls.static import static
import django.contrib
from django.urls import include, path
from django.views.defaults import page_not_found
from django.views.generic.base import RedirectView

from lyceum import settings

__all__ = []


def custom_page_not_found(request):
    return page_not_found(request, None)


def favicon_url():
    return (
        RedirectView.as_view(
            url=django.contrib.staticfiles.storage.staticfiles_storage.url(
                'img/favicon.ico',
            ),
        ),
    )


urlpatterns = [
    path('favicon.ico/', favicon_url),
    path('', include('homepage.urls')),
    path('about/', include('about.urls')),
    path('admin/', django.contrib.admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('catalog/', include('catalog.urls')),
    path('download/', include('download.urls')),
    path('feedback/', include('feedback.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns.append(
        path('404/', custom_page_not_found),
    )  # Для проверки 404.html при Debug=True
    debug_toolbar = import_module('debug_toolbar.toolbar')
    urlpatterns += debug_toolbar.debug_toolbar_urls()
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
