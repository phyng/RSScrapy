
from django import template
register = template.Library()

@register.simple_tag
def active(request, pattern):
    import re
    #assert False
    if pattern == request.path:
        return 'active'
    else:
        return ''
