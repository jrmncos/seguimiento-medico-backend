from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushResponseError,
    PushServerError,
) 
from requests.exceptions import ConnectionError, HTTPError
from api.models import User
import json

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
                self.send_push_message(token=user.expo_token, message=notificacion.titulo, extra=url_json)


    # Basic arguments. You should extend this function with the push features you
    # want to use, or simply pass in a `PushMessage` object.
    def send_push_message(self, token, message, extra=None):
        try:
            response = PushClient().publish(
                PushMessage(to=token,
                            body=message,
                            data=extra))
        except PushServerError as exc:
            # Encountered some likely formatting/validation error.
            """
            rollbar.report_exc_info(
                extra_data={
                    'token': token,
                    'message': message,
                    'extra': extra,
                    'errors': exc.errors,
                    'response_data': exc.response_data,
                })
            """
            raise
        except (ConnectionError, HTTPError) as exc:
            # Encountered some Connection or HTTP error - retry a few times in
            # case it is transient.
            """
            rollbar.report_exc_info(
                extra_data={'token': token, 'message': message, 'extra': extra})
            """
            raise #self.retry(exc=exc)

        try:
            # We got a response back, but we don't know whether it's an error yet.
            # This call raises errors so we can handle them with normal exception
            # flows.
            response.validate_response()
        except DeviceNotRegisteredError:
            # Mark the push token as inactive
            from notifications.models import PushToken
            PushToken.objects.filter(token=token).update(active=False)
        except PushResponseError as exc:
            # Encountered some other per-notification error.
            """
            rollbar.report_exc_info(
                extra_data={
                    'token': token,
                    'message': message,
                    'extra': extra,
                    'push_response': exc.push_response._asdict(),
                })
            """
            raise #self.retry(exc=exc)