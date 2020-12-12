from django.db import models

from .user import User
from .paciente import Paciente

class ProfesionalDeSalud(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profesional_profile')
    pacientes = models.ManyToManyField(Paciente, related_name='paciente_list', blank=True)
    
    def __str__(self):
        return "{} | {} | {}".format(self.user.dni, self.user.first_name, self.pacientes)