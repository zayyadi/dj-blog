# In blog/templatetags/blog_extras.py
from django import template

register = template.Library()


# NEW: The missing split filter
@register.filter(name='split')
def split(value, key=' '):
    """
    Returns the value turned into a list.
    E.g. "a b c"|split will be ['a', 'b', 'c']
    """
    return value.split(key)

@register.filter
def get_digit(value, arg):
    """Returns the digit of a number. Can be used as a list index."""
    try:
        return value[int(arg)]
    except (IndexError, TypeError, ValueError):
        return value[0] # Default to the first item on error


