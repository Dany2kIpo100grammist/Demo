from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class SplitCharField(forms.Field):
    def __init__(self, separator='', max_items=3, strip=True, *args, **kwargs):
        self.separator = separator
        self.max_items = max_items
        self.strip = strip
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return []
        parts = value.split(self.separator)
        if self.strip:
            parts = [p.strip() for p in parts]
        
        parts = [p for p in parts if p]
        
        if self.max_items is not None and len(parts) != self.max_items:
            raise ValidationError(_("Введите свои ФИО"))
        
        return parts