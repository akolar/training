from django import template
from django.core import urlresolvers
from activities.urls import SORT_DEFAULTS

register = template.Library()


@register.simple_tag(takes_context=True)
def urlfilter(context, key=None, keep_inversion=False, page=1):
    resolved = urlresolvers.resolve(context.get('request').path)
    current_key = resolved.kwargs.get('key', 'date')
    current_inv = bool(resolved.kwargs.get('inverted', '-'))

    key = current_key if not key else key
    inverted = SORT_DEFAULTS[key]
    if key == current_key:
        inverted = not current_inv

    if keep_inversion:
        inv_str = '-' if current_inv else ''
    else:
        inv_str = '' if current_inv else '-'

    return urlresolvers.reverse('activities:view-all-sorted', kwargs={'key': key, 'inverted': inv_str, 'page': page})
