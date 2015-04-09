from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView


urlpatterns = patterns('user_settings.views',  # noqa
    url(r'^$', RedirectView.as_view(url=reverse_lazy('settings:me')), name='index'),
    url(r'language/(?P<language>\w{2})', 'set_language', name='set-lang'),
    url(r'^me$', 'about', name='me'),
    url(r'^equipment/add/(?P<type_>(bike|shoes|other))/(?P<id_>\d+)', 'equipment_add', name='equipment_add'),
    url(r'^equipment/add/(?P<type_>(bike|shoes|other))', 'equipment_add', name='equipment_add'),
    url(r'^equipment$', 'equipment', name='equipment'),
    url(r'^account$', 'account', name='account'),
    url(r'^save/avatar$', 'avatar_save', name='avatar'),
    url(r'^save/(?P<key>\w+)$', 'settings_save', name='save'),
) + patterns('health.views',
    url(r'^performance', 'settings', name='performance')
)
