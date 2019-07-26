from django import template

register = template.Library()

@register.simple_tag
def is_selected(value, num):
    if value is num:
        return 'selected'

@register.filter
def get_item(value):
    print(value)
    print([i for i in value])


    return 'x.x'
