from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from user.models import User, Request
from app import settings

from lib.forms import SplitCharField
from lib.validators import RussianPhoneNumberValidator

# Готовая форма для логина. 
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "password"
        )
        
    username = forms.CharField(
        label="Логин",
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput()
    )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "fio",
            "phonenumber"
        )
    
    username = forms.CharField(
        label="Логин"
    )
    email = forms.CharField(
        label="Эл. почта"
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        widget=forms.HiddenInput(), 
        required=False
    )
    fio = SplitCharField(
        separator=" ",
        max_items=3,
        strip=True,
        label="ФИО"
    )
    phonenumber = forms.CharField(
        label="Номер телефона",
        validators=[RussianPhoneNumberValidator()]
    )
    
class MakeRequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = (
            "address",
            "phonenumber",
            "date",
            "service",
            "isCustom",
            "customService",
        )
        
    address = forms.CharField(
        label="Адрес",
        required=True
    )
    phonenumber = forms.CharField(
        label="Номер телефона",
        required=True,
        widget=forms.TextInput(attrs={
            "autocomplete": "tel"
        }),
        validators=[RussianPhoneNumberValidator()]
    )
    date = forms.DateTimeField(
        label="Дата клининга",
        required=True,
        widget=forms.DateTimeInput(attrs={
            "type": "datetime-local",
        })
    )
    service = forms.ChoiceField(
        label="Тип услуг",
        choices=list(settings.SERVICE_TYPES.items()),
    )
    isCustom = forms.BooleanField(
        label="Своя услуга",
        required=False,
        widget=forms.CheckboxInput(attrs={
            "class": "show-element",
            "data-for-what-elements": "hidden-element",
        })
    )
    customService = forms.CharField(
        label="Иная услуга",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "hidden-element"
        })
    )