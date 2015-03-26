from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static

from training.settings import DEBUG, MEDIA_URL, MEDIA_ROOT


urlpatterns = patterns('',  # noqa
    url(r'^', include('presentation.urls')),
    url(r'^health/', include('health.urls', namespace='health')),
    url(r'^activities/', include('activities.urls', namespace='activities')),
    url(r'^goals/', include('goals.urls', namespace='goals')),

    url(r'^settings/', include('user_settings.urls', namespace='settings')),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),
    url(r'^admin/', include(admin.site.urls)),
)

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
