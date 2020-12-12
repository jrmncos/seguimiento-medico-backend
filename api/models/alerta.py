from django.db import models

from .autocontrol import ACDiabetes

class AlertaACDiabetes(models.Model):
    autocontrol_diabetes = models.OneToOneField(ACDiabetes, on_delete=models.CASCADE, related_name='alerta')
    detalles = models.CharField(max_length=1024)
    
    def __str__(self):
        return "ACDiabetes: "+str(self.autocontrol_diabetes.id)+", Detalle: "+str(self.detalles)