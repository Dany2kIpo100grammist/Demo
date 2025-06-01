import re

from django import template

register = template.Library()

@register.filter()
def format_russian_number(value: str):
    pattern = re.compile(r"\(|\)| |-|(^\+7|^8)")
    result = re.sub(pattern, "", value)
    
    return f"+7({result[:3]})-{result[3:6]}-{result[6:8]}-{result[8:10]}"