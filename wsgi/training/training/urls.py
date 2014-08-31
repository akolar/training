from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',  # noqa
    url(r'^', include('presentation.urls')),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
)
