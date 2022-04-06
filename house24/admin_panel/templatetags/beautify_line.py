from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.filter(name='beauty_error')
def beauty_filter(value):
    text = value.replace('* ', '')
    return text


@register.filter(name='beauty_error_tag')
def beauty_filter(value):
    tags = {
        '__all__': _('Error')
    }
    return tags[value] if value in tags.keys() else value


@register.filter(name='prepare_error_message')
def prepare_message(value):
    result = {}
    if isinstance(value, list):
        for item in value:
            for key, value in item.items():
                result[key] = value
    elif isinstance(value, dict):
        result.update(value)
    return result


@register.filter(name='filter_none')
def filter_none(value):
    if not value:
        return _('Not specified')
    return value
