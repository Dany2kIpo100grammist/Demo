import re

from django.db import models
from django.contrib.auth.models import AbstractUser

from app import settings

from lib.validators import RussianPhoneNumberValidator
from lib.utils import format_russian_number

class User(AbstractUser):
    first_name = None
    last_name = None
    fio = models.CharField(verbose_name="ФИО", blank=True, max_length=64)
    phonenumber = models.CharField(verbose_name="Номер телефона", blank=True, null=True, max_length=17,
                                   validators=[RussianPhoneNumberValidator()])
    
    class Meta:
        db_table = "user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        
    def save(self, *args, **kwargs):
        if self.phonenumber: self.phonenumber = format_russian_number(self.phonenumber)
            
        super().save(*args, **kwargs)
        #+7(XXX)-XXX-XX-XX
        
    def __str__(self): return self.fio

class Request(models.Model):
    class StatusTypes(models.TextChoices):
        NEW = "new", "Новая заявка",
        DONE = "done", "Услуга оказана",
        CANCELLED = "cancelled", "Услуга отменена"
        
    class PayTypes(models.TextChoices):
        CASH = "cash", "Наличные",
        CARD = "card", "Банковская карта"
        
    # Вторичные ключи на другие модели
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="requests")
    
    address = models.TextField(verbose_name="Адрес", blank=False)
    phonenumber = models.CharField(verbose_name="Номер телефона", blank=False,
                                   validators=[RussianPhoneNumberValidator()])
    service = models.CharField(verbose_name="Тип услуг", blank=False, max_length=32)
    date = models.DateTimeField(verbose_name="Дата получения услуги", blank=False)
    createdAt = models.DateTimeField(verbose_name="Дата создания заявки", auto_now_add=True)
    isCustom = models.BooleanField(verbose_name="Своя услуга?", default=False)
    status = models.CharField(verbose_name="Статус заявки", blank=False, choices=StatusTypes.choices, default=StatusTypes.NEW)
    payType = models.CharField(verbose_name="Тип оплаты", blank=False, choices=PayTypes.choices, default=PayTypes.CASH)
    # customService = models.CharField(verbose_name="Своя услуга", blank=True, max_length=64)
    
    class Meta:
        db_table = "request"
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        
    def save(self, *args, **kwargs):
        # Срабатывает в том случае если пользователь не указал номер телефона в форме. Номер телефона всё равно будет указан
        if not self.phonenumber and self.user:
            self.phonenumber = self.user.phonenumber
        
        super().save(*args, **kwargs)
        
    def __str__(self): return f"Заявка от {self.user.fio} - {self.service}"