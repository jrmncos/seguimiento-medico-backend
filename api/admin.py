from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(ECNT)
admin.site.register(Paciente)
admin.site.register(AutocontrolDiabetes)
admin.site.register(ProfesionalDeSalud)