from django import template
from django.core import urlresolvers


register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, *args):
    """Returns 'active' if passed page is open."""

    matches = _current_url_equals(context, *args)
    return ' active' if matches else ''


def _current_url_equals(context, *args):
    for key in args:
        try:
            resolved = urlresolvers.resolve(context.get('request').path)
            if '{}:{}'.format(resolved.namespace, resolved.url_name) == key:
                return True
        except:
            pass

    return False
