from django.db import models

from .paciente import Paciente

class ACDiabetes(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="autocontrol_diabetes")
    glucemia_matutina = models.BooleanField(null = True,)
    opcional_glucemia_matutina = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    glucemia_post_comida_principal = models.BooleanField(null = True)
    opcional_glucemia_comida_principal = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fecha_hora_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Glucemia matutina: " + str(self.glucemia_matutina) + "Glucemia post comida principal: " + str(self.glucemia_post_comida_principal)

class ACDiabetesOpcional(models.Model):
    autocontrol_diabetes = models.OneToOneField(ACDiabetes, on_delete=models.CASCADE, related_name='autocontrol_opcional')
    aumento_fatiga = models.BooleanField(blank=True)
    perdida_memoria = models.BooleanField(blank=True)
    cambio_orina = models.BooleanField(blank=True)
    perdida_vision = models.BooleanField(blank=True)