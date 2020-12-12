from django.db import models

from .user import User
from .ecnt import ECNT

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='paciente_profile')
    ultimo_autocontrol = models.DateTimeField(null=True)
    ecnts = models.ManyToManyField(ECNT, related_name='paciente_list', blank=True)

    def __str__(self):
        return "{} | {}".format(self.user.dni, self.user.first_name)