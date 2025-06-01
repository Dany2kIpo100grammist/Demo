from django import template

register = template.Library()

@register.filter()
def contains(value, arg: dict):
    if hasattr(arg, '__iter__') and not isinstance(arg, str):
        return value in arg
    return value == arg