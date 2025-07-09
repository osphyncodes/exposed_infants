from django import template

register = template.Library()

@register.filter
def get_field_display(obj, field_name):
    try:
        return getattr(obj, f"get_{field_name}_display")()
    except AttributeError:
        return getattr(obj, field_name)

@register.filter
def age_in_months(visit_date, dob):
    """
    Returns the number of months between dob and visit_date, counting the current month if the day has passed.
    The month of birth is counted as 0, but if the visit day is the same or after the birth day, add 1.
    """
    if not visit_date or not dob:
        return ""
    try:
        months = (visit_date.year - dob.year) * 12 + (visit_date.month - dob.month)
        if visit_date.day >= dob.day:
            months += 1
        return max(months, 0)
    except Exception:
        return ""
