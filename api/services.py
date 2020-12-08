from .push_notifications import *
from .models import User, AlertaACDiabetes, Paciente
from .serializers import PacienteSerializer
import json
from datetime import datetime
from datetime import date
from rest_framework.response import Response
from django.utils import timezone

class AutocontroladorService:
    def check_ultimo_autocontrol(self):
        print("Voy a controlar a les pacientes")
        pacientes = Paciente.objects.all()
        for paciente in pacientes:
            print(paciente.ultimo_autocontrol.date())
            delta = timezone.now().date() - paciente.ultimo_autocontrol.date()
            print(delta)
            if delta.days > 1:
                print("No se realizo el autocontrol de hoy")
                send_push_message(token=paciente.user.expo_token, message="Por favor ingresa tu autocontrol diario")

class AlertaACDiabetesService:
    def check_autocontrol(self, autocontrol):
        if(not autocontrol.glucemia_matutina or not autocontrol.glucemia_post_comida_principal):
            today = date.today()
            detalleAlerta = "Autocontrol: "+str(today.strftime("%d/%m/%Y"))+", valores de glucosa anormales."

            alertaPredefinida = None
            alertas = AlertaACDiabetes.objects.all()
            
            for alerta in alertas:
                if(alerta.autocontrol_diabetes_id == autocontrol.id):
                    alertaPredefinida = alerta

            if(alertaPredefinida == None):
                alertaPredefinida = AlertaACDiabetes.objects.create(autocontrol_diabetes=autocontrol, 
                detalles=detalleAlerta)

            paciente = Paciente.objects.filter(id = autocontrol.paciente_id).first()
            
            if(paciente.user.expo_token != ""):
                send_push_message(token=paciente.user.expo_token, message=alertaPredefinida.detalles)

class NotificadorService:
    def send_notificacion(self, notificacion):
        print("Les voy a enviar la notificacion a todes.")
        print(str(notificacion))
        url = {
            "url": notificacion.imagen.url
        }
        url_json = json.dumps(url)
        print(url_json)
        users = User.objects.all()
        for user in users:
            print("EXPO TOKEN: "+user.expo_token)
            if(user.expo_token != ""):
                send_push_message(token=user.expo_token, message=notificacion.titulo, extra=url_json)
            
            
