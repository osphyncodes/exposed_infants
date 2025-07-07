from django import template

register = template.Library()

@register.filter
def get_field_display(obj, field_name):
    try:
        return getattr(obj, f"get_{field_name}_display")()
    except AttributeError:
        return getattr(obj, field_name)
