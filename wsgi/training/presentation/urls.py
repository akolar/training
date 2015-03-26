from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('presentation.views',  # noqa
    url(r'^$', 'index', name='home')
)
