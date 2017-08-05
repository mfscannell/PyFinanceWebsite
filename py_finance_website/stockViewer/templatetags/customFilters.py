from django import template

register = template.Library()


@register.filter(name='index')
def index(value, arg):
    return value[int(arg)]

@register.filter(name='keyValue')
def keyValue(dict, key):
    return dict[key]
