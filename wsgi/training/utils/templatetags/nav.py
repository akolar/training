from django import template
from django.core import urlresolvers


register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, *args):
    matches = current_url_equals(context, *args)
    return ' active' if matches else ''


def current_url_equals(context, *args):
    resolved = False

    for key in args:
        try:
            resolved = urlresolvers.resolve(context.get('request').path)
            if resolved.url_name == key:
                return True
        except:
            pass

    return False
