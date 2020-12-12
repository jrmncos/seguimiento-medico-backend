from django.db import models

class ECNT(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=1024)
    def __str__(self):
        return str(self.nombre)