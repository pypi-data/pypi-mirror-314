from django import template

from livesettings.conf import livesettings


register = template.Library()


@register.simple_tag
def get_setting(key):
    return getattr(livesettings, key)
