from django import template

register = template.Library()

@register.filter
def modulo(num, val):
    return num % val

@register.filter
def rest_range(num, val):
    return range(0, num[0][1] % val - 1)

@register.filter
def times(number):
    return range(number)