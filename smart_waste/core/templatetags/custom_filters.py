from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplies the value by the given argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
    
@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})