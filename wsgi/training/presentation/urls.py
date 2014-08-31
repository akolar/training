from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import IndexView

urlpatterns = patterns('presentation.views',  # noqa
    url(r'^$', IndexView.as_view(), name='home')
)
