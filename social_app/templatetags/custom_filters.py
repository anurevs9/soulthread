from django import template

register = template.Library()

@register.filter(name='is_image')
def is_image(value):
    return value.lower().endswith(('.jpg', '.jpeg', '.png'))