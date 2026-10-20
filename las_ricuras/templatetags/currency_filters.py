from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def cop(value):
    try:
        precio = Decimal(str(value))
        precio = int(precio)
        return f" {precio:,}".replace(",",".")
    except (ValueError, TypeError,InvalidOperation):
        return value