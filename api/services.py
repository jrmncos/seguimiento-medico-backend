from .push_notifications import *

class AutocontrolDiabetesService:
    def check_autocontrol(self, autocontrol):
        print("Entre aca!")
        send_push_message(token="ExponentPushToken[JdQCN9J3DdXe_t6uBhV3jJ]", message="Soy la segunda notificacion push")

