from django.conf.urls import url
from bnlipsum.lyrics.views import lipsum

urlpatterns = [
    url('^$', lipsum, name='lipsum')
]
