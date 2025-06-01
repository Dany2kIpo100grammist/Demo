import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RussianPhoneNumberValidator():
    def __init__(self):
        self.pattern = re.compile(r"\(|\)| |-|(^\+7|^8)")
    
    def __call__(self, value):
        result = re.sub(self.pattern, "", value)
            
        if len(result) != 10:
            raise ValidationError(_("Номер телефона слишком короткий/длинный"))
        
    def __eq__(self, other):
        """Необходимо для @deconstructible"""
        return isinstance(other, RussianPhoneNumberValidator)

    def deconstruct(self):
        return ('user.validators.RussianPhoneNumberValidator', [], {})