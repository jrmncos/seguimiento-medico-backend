from celery import shared_task
from .services import AutocontroladorService

@shared_task
def add(x, y):
    print('Hii')
    return x + y

@shared_task
def mul(x, y):
    return x * y

@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def autocontrolador():
    autocontrolador_service = AutocontroladorService()
    autocontrolador_service.check_ultimo_autocontrol()
