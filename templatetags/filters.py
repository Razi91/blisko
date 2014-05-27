# -*- coding: utf-8 -*-
__author__ = 'Artur'

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='percent')
def percent(value):
    try:
        return "%2d%%" % (value * 100)
    except (ValueError, ZeroDivisionError):
        return ""