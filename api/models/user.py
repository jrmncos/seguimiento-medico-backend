from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group

import datetime

from api.managers import UserManager

GENDER_CHOICES = (
    ('Femenino', 'Femenino'),
    ('Masculino', 'Masculino')
)

class User(AbstractBaseUser, PermissionsMixin):
 
    email = models.EmailField(_('email address'), blank=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    bod = models.DateField()
    dni = models.IntegerField(unique=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=15)
    longitude = models.DecimalField(max_digits=20, decimal_places=15)
    expo_token = models.CharField(max_length=100)
    gender = models.CharField(max_length=9, choices=GENDER_CHOICES, default='F')

    objects = UserManager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def get_edad(self):
        import datetime
        return datetime.date.today() - self.bod
    
    def __str__(self):
       return str(self.dni) +" "+ str(self.first_name)