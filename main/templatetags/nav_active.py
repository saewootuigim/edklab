from django import template
from django.urls import resolve

register = template.Library()

@register.simple_tag
def active_url(request, url_name):
    if resolve(request.path_info).url_name == url_name:
        return "active"
    return ""
