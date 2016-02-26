"""
bnlipsum URL Configuration
"""

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('bnlipsum.lyrics.urls'))
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.static import serve

    urlpatterns += staticfiles_urlpatterns() + [
        url(
            r'^media/(?P<path>.*)$', serve,
            {
                'document_root': settings.MEDIA_ROOT
            }
        )
    ]
