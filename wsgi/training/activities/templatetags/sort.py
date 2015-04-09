from django import template
from django.core import urlresolvers

register = template.Library()


@register.simple_tag(takes_context=True)
def urlfilter(context, key=None, keep_inversion=False, page=1):
    """Changes the current url using the provided directives.
    Arguments:
        key: data is ordered by `key`; set to `None` to keep current key
        keep_inversion: true if you want keep the direction of sorting
        page: current page position
    """

    resolved = urlresolvers.resolve(context.get('request').path)

    # Get current settings
    current_key = resolved.kwargs.get('key', 'date')
    current_inv = bool(resolved.kwargs.get('inverted', '-'))

    key = current_key if not key else key

    if keep_inversion:
        inv_str = '-' if current_inv else ''
    else:
        inv_str = '' if current_inv else '-'

    return urlresolvers.reverse('activities:view-all-sorted', kwargs={'key': key, 'inverted': inv_str, 'page': page})
