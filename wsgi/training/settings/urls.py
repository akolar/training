from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView


urlpatterns = patterns('settings.views',  # noqa
    url(r'^$', RedirectView.as_view(url=reverse_lazy('settings_me')),
        name='settings_index'),
    url(r'^me$', 'about', name='settings_me'),
    url(r'^equipment$', 'equipment', name='settings_equipment'),
    url(r'^account$', 'account', name='settings_account'),
    url(r'^save/avatar$', 'avatar_save', name='settings_avatar'),
    url(r'^save/(?P<key>\w+)$', 'settings_save', name='settings_save'),
) + patterns('health.views',
    url(r'^performance', 'settings', name='settings_performance')
)
