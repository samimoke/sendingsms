import random
import string
from django import template

register = template.Library()

@register.filter
def random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for _ in range(length)))