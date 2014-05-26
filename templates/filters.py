# -*- coding: utf-8 -*-
__author__ = 'Artur'

@register.filter
def percent(value):
    try:
        return "%2d%%" % (value * 100)
    except (ValueError, ZeroDivisionError):
        return ""