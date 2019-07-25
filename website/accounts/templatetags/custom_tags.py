from django import template

register = template.Library()

@register.simple_tag
def is_selected(value, num):
    if value is num:
        return 'selected'
    
