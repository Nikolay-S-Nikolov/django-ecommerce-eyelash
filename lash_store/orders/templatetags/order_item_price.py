from django import template

register = template.Library()


@register.filter
def divide(value, arg):
    return f'{(value / arg):.2f}'
