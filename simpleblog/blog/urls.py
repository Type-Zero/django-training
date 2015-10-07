from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^articles/(?P<slug>\S+)$', views.article, name='details'),
]