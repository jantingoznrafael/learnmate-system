from django import template
from questions.utils import time_ago

register = template.Library()


@register.filter(name='time_ago')
def time_ago_filter(dt):
    """Template filter for time_ago utility."""
    return time_ago(dt)


@register.filter
def mul(value, arg):
    """Multiply the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

