# apps/content/templatetags/snippet_filters.py
from django import template

register = template.Library()


@register.filter(name="splitlines")
def splitlines(value):
    """Split a string into a list of lines."""
    if not value:
        return []
    return str(value).split("\n")


@register.filter(name="linecount")
def linecount(value):
    """Count lines in a string."""
    if not value:
        return 0
    return str(value).count("\n") + 1
