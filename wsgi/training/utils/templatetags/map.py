from datetime import time
from django import template

from utils.helpers import average, CONVERT_KM_MILE
from activities import ureg

register = template.Library()


def __convert(value):
    if type(value) is time:  # pace
        seconds = value.hour * 3600 + value.minute * 60 + value.second
        seconds /= CONVERT_KM_MILE

        second = seconds % 60
        minute = seconds // 60

        return time(int(minute // 60) % 23, int(minute % 60), int(second))

    elif value.units == (ureg.km / ureg.hour).units:  # speed
        return value.to(ureg.mile / ureg.hour)

    elif value.units == (ureg.meter).units:  # distance (short)
        return value.to(ureg.feet)

    elif value.units == (ureg.km).units:  # distance (long)
        return value.to(ureg.mile)

    return value


@register.simple_tag
def average_values(values, devide_by=1, avg_range=10, precision=2):
    """Averages values in specified range.
    Arguments:
        devide_by: devide each value by this numbers
        avg_range: number of previous values to average from
        precision: number of decimal places
    """

    if devide_by != 1:
        values = map(lambda x: float(x) / devide_by, values)

    if avg_range != 1:
        values = map(lambda x: average(values[0:x]) if x < avg_range else average(values[x - avg_range:x]),
                     range(1, len(values) + 1))

    return map(lambda x: round(x, precision), values)


@register.simple_tag(takes_context=True)
def units(context, value, precision=0):
    """Formats the pint object to string with units.
    Arguments:
        value: pint object
        precision: number of decimal places
    """

    if not value:
        return 'n/a'

    if not context['request'].user.details.si_units:
        value = __convert(value)

    return '{{:.0{}f~}}'.format(precision).format(value)


@register.simple_tag(takes_context=True)
def pace(context, value):
    """Formats the number to appropriate pace format.
    Arguments:
        value: pace
    """

    if not context['request'].user.details.si_units:
        value = __convert(value)

    return '{}:{:02d}'.format(value.hour * 60 + value.minute, value.second)


@register.filter
def fahrenheit(value):
    """Converts temperature to fahrenheit.
    Arguments:
        value: temperature in degrees celcius
    """

    return '{:~}'.format(value.to(ureg.fahrenheit))


@register.simple_tag(takes_context=True)
def per_km(context):
    """Returns selected distance value."""

    return 'km' if context['request'].user.details.si_units else 'mi'
