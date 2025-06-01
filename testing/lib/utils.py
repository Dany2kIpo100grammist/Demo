import re

from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

def format_russian_number(number):
    if not number: return number
    
    pattern = re.compile(r"\(|\)| |-|(^\+7|^8)")

    result = re.sub(pattern, "", number)
    
    if len(result) == 10:
        number = f"+7({result[:3]})-{result[3:6]}-{result[6:8]}-{result[8:10]}"
    else:
        raise ValidationError(_("Номер телефона слишком короткий/длинный"))
    
    return f"+7({result[:3]})-{result[3:6]}-{result[6:8]}-{result[8:10]}"