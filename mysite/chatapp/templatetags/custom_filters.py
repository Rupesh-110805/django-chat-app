from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Split string by separator"""
    return value.split(arg)
