import re

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

# The PI's name however an author list spells it, e.g. "Eun Deok Kim" or "Eun-Deok Kim".
PI_NAME = re.compile(r'Eun[\s\S]*?Deok[\s\S]*?Kim')


@register.filter(needs_autoescape=True)
def bold_pi(authors, autoescape=True):
    """Escape an author list and bold its first mention of the PI as "Eun-Deok Kim"."""
    if autoescape:
        authors = conditional_escape(authors)
    return mark_safe(PI_NAME.sub('<strong>Eun-Deok Kim</strong>', authors, count=1))
