from django import template

register = template.Library()

@register.filter
def filter_status(baskets, status):
    """Filter baskets by status"""
    return [basket for basket in baskets if basket.status == status] 