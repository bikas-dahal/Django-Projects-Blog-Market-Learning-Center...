from django import template
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe



register = template.Library()
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))