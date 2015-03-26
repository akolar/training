from django.conf.urls import patterns, include, url


urlpatterns = patterns('goals.views',  # noqa
    url(r'set/(?P<target>week|month|year)', 'set', name='set')
)
