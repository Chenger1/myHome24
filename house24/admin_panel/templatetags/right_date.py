from django import template

import datetime


register = template.Library()


@register.filter(name='valid_date_format')
def valid_date_format(value):
    return datetime.datetime.strftime(value, '%Y-%m-%d')
