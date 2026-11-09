from django import template

register = template.Library()


@register.simple_tag
def active_url(request, url_name):
    # Reuse the URL match Django already made for this request.
    if getattr(request.resolver_match, 'url_name', None) == url_name:
        return "active"
    return ""
