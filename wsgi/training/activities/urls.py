from django.conf.urls import patterns, include, url
from activities.views import ORDER_KEYS


SORT_DEFAULTS = {
    'date': True,
    'title': False,
    'sport': False,
    'distance': True,
    'elevation': True,
    'time': True,
    'speed': True,
    'hr': False,
    'temperature': False,
    'rpe': False
}


urlpatterns = patterns('activities.views',  # noqa
    url(r'^overview$', 'overview', name='overview'),
    url(r'^$', 'view_all', name='view-all'),
    url(r'^status=(?P<status>\w+)$', 'view_all', name='view-all-status'),
    url(r'^sorted=(?P<inverted>-?)(?P<key>{}),(?P<page>\d+)$'.format('|'.join(ORDER_KEYS.keys())), 'view_all',
        name='view-all-sorted'),
    url(r'^summary$', 'summary', name='summary'),

    url(r'^upload/manual$', 'manual_entry', name='manual-entry'),
    url(r'^upload$', 'upload', name='upload'),
    url(r'^delete/(?P<id_>\d+)$', 'delete', name='delete'),
    url(r'^edit/(?P<id_>\d+)$', 'edit', name='edit'),

    url(r'^view/(?P<id_>\d+)$', 'view', name='view'),
    url(r'^charts/(?P<id_>\d+)$', 'charts', name='charts'),
    url(r'^zones/(?P<id_>\d+)$', 'zones', name='zones'),
    url(r'^splits/(?P<id_>\d+)$', 'splits', name='splits'),
    url(r'^map/(?P<id_>\d+)$', 'map_', name='map'),

    url(r'^api/ochart/(?P<id_>\d+)$', 'ochart', name='ochart'),
    url(r'^api/map/(?P<id_>\d+)$', 'map_data', name='map-data'),
    url(r'^api/chart/(?P<id_>\d+)/(?P<data_type>\w+)$', 'chart_data', name='chart-data'),
    url(r'^api/zones/(?P<id_>\d+)/(?P<data_type>\w+)$', 'zones_data', name='zones-data'),
    url(r'^api/track/(?P<id_>\d+)$', 'track', name='track'),
    url(r'^api/summary/(?P<period>week|month|year)$', 'period_summary', name='period-summary'),
    url(r'^api/wchart$', 'week_chart', name='week-chart'),
)
