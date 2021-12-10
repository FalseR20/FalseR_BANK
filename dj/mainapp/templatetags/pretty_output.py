from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def pretty_output(number: str) -> str:
    out = "%s %s %s %s" % (number[:4], number[4:8], number[8:12], number[12:])
    return out


@register.filter
def cut_cardholder_name(txt: str, count: int) -> str:
    out = txt[:count] + "..." if len(txt) > count else txt
    return out
