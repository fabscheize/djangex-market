from importlib import import_module

from django.conf.urls.static import static
import django.contrib
from django.urls import include, path
import django.views

from lyceum import settings

__all__ = []


def custom_page_not_found(request):
    return django.views.defaults.page_not_found(request, None)


urlpatterns = [
    path('admin/', django.contrib.admin.site.urls),
    path(
        'favicon.ico/',
        django.views.generic.base.RedirectView.as_view(
            url=django.contrib.staticfiles.storage.staticfiles_storage.url(
                'img/favicon.ico',
            ),
        ),
    ),
    path('', include('homepage.urls')),
    path('about/', include('about.urls')),
    path('catalog/', include('catalog.urls')),
    path('download/', include('download.urls')),
    path('feedback/', include('feedback.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
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
