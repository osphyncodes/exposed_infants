# tracing/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_chart_color(index):
    colors = ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#858796', '#f8f9fc', '#5a5c69']
    return colors[index % len(colors)]

@register.filter
def divisible(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0