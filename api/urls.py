from django.conf.urls import url, include
from rest_framework import routers
from .views import UserViewSet, ECNTViewSet
#from rest_framework.authtoken.views import obtain_auth_token  # <-- Here
from api.auth.views import obtain_auth_token
from django.urls import path

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'ecnts', ECNTViewSet, basename='ecnt')
#router.register(r'token', ObtainAuthToken, basename='token')

urlpatterns = [
    url(r'^', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # <-- And here
]