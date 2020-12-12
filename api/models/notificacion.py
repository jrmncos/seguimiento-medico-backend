from django.db import models

class Notificacion(models.Model):
    titulo = models.CharField(max_length=150)
    imagen = models.ImageField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.imagen.url) 