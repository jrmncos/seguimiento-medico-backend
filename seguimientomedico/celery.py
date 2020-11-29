#Activamos los imports absolutos para evitar conflictos entre packages

import os

from celery import Celery

from django.conf import settings
from django.apps import apps
#indicamos el Django settings module por defecto para nuestro programa celery (no es necesario pero asi evitamos tener que pasarle siempre al programa celery nuestro módulo settings)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seguimientomedico.settings')

app = Celery('seguimientomedico')

#Añadimos el Django settings module como fuente de configuración de Celery (nos permite configurar Celery directamente desde el Django settings). Al pasarlo como string nos ahorramos un problema si trabajasemos con windows.
app.config_from_object(settings, namespace='CELERY')

# Si tenemos nuestras tareas en un fichero de nombre tasks.py, esto nos permite indicarle a celery que encuentre automáticamente dicho módulo dentro del proyecto. De este modo no tenemos que añadirlo a la variable CELERY_IMPORTS del settings
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) Deberia funcar pero no
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
#ejemplo de tarea que muestra su propia información. El bind=True indica que hace referencia a su instancia de tarea actual.
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
