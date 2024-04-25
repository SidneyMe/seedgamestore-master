from django import template

register = template.Library()

@register.simple_tag
def concat(*args):
    return ''.join(map(str, args))