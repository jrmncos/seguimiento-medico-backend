from django.conf.urls import url, include
from rest_framework import routers
from .views import UserViewSet, ECNTViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'ecnts', ECNTViewSet, basename='ecnt')
urlpatterns = [
    url(r'^', include(router.urls)),
    #url(r'^auth/', include('rest_auth.urls')),
]