from .push_notifications import *
from .models import User
import json

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
            if(user.expo_token != None):
                send_push_message(token=user.expo_token, message=notificacion.titulo, extra=url_json)
            
            
