from django.conf.urls import patterns, url


urlpatterns = patterns('strava.views',  # noqa
    url(r'^connect$', 'connect', name='connect'),
    url(r'^callback$', 'callback', name='callback'),
    url(r'^disconnect$', 'disconnect', name='disconnect')
)
