from django import template
import os

register = template.Library()

@register.filter
def basepath(value):
    return os.path.basename(value)
