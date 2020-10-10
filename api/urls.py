from django.conf.urls import url, include
from rest_framework import routers
from .views import UserViewSet, ECNTViewSet, PacienteViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'ecnts', ECNTViewSet)
router.register(r'pacientes', PacienteViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    #url(r'^auth/', include('rest_auth.urls')),
]