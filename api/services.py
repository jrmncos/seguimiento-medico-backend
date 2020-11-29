from .push_notifications import *
from .models import User, AlertaACDiabetes, Paciente
import json

class AlertaACDiabetesService:
    def check_autocontrol(self, autocontrol):
        if(not autocontrol.glucemia_matutina or not autocontrol.glucemia_post_comida_principal):
            alertaPredefinida = None
            alertas = AlertaACDiabetes.objects.all()
            
            for alerta in alertas:
                if(alerta.autocontrol_diabetes_id == autocontrol.id):
                    alertaPredefinida = alerta

            if(alertaPredefinida == None):
                alertaPredefinida = AlertaACDiabetes.objects.create(autocontrol_diabetes=autocontrol, detalles="Sus valores de glucosa no son normales, considere acudir a un médico")
           
            paciente = Paciente.objects.filter(id = autocontrol.paciente_id).first()
            
            if(paciente.user.expo_token != ""):
                send_push_message(token=paciente.user.expo_token, message=alertaPredefinida.detalles)

class AutocontrolDiabetesService:
    def check_autocontrol(self, autocontrol):
        print("Entre aca!")
        send_push_message(token="ExponentPushToken[JdQCN9J3DdXe_t6uBhV3jJ]", message="Soy la segunda notificacion push")

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
            
            
