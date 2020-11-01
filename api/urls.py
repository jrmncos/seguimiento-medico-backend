from django.conf.urls import url, include
from rest_framework import routers
from .views import *
#from rest_framework.authtoken.views import obtain_auth_token  # <-- Here
#from api.auth.views import obtain_auth_token
from django.urls import path
from django.conf import settings
router = routers.SimpleRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'ecnts', ECNTViewSet, basename='ecnt')
router.register(r'pacientes', PacienteViewSet, basename='paciente')
router.register(r'acdiabetes', AutocontrolDiabetesViewSet, basename='acdiabetes')
#router.register(r'token', ObtainAuthToken, basename='token')

urlpatterns = [
    url(r'^', include(router.urls)),
    #path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('notification/', NotificacionView.as_view() )  # <-- And here
]
