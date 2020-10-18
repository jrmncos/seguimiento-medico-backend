from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'))
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    
    bod = models.DateField(blank=True, null=True)
    dni = models.IntegerField(unique=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=16, blank=True, null=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
    
    def __str__(self):
       return str(self.dni) + str(self.first_name)
    
class ECNT(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return str(self.nombre)

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='paciente_profile')
    ultimo_autocontrol = models.CharField(max_length=30, null=True)
    ecnts = models.ManyToManyField(ECNT, related_name='paciente_list', blank=True)

    def __str__(self):
        return "{} | {}".format(self.user.dni, self.user.first_name)

class AutocontrolDiabetes(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    glucemia_matutina = models.BooleanField()
    glucemia_post_comida_principal = models.BooleanField()
    hora_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Glucemia matutina: " + str(glucemia_matutina) + "Glucemia post comida principal: " + str(glucemia_post_comida_principal)

class AutocontrolDiabetesExtra(models.Model):
    autocontrol_diabetes = models.OneToOneField(AutocontrolDiabetes, on_delete=models.CASCADE)
    aumento_fatiga = models.BooleanField(blank=True)
    perdida_memoria = models.BooleanField(blank=True)
    cambio_orina = models.BooleanField(blank=True)
    perdida_vision = models.BooleanField(blank=True)