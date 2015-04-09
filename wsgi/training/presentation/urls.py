from django.conf.urls import patterns, url


urlpatterns = patterns('presentation.views',  # noqa
    url(r'^$', 'index', name='home')
)
