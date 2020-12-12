from rest_framework import viewsets, mixins, generics, permissions

from api.models import ECNT
from api.serializers import ECNTSerializer

class ECNTViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ECNT.objects.all()
    serializer_class = ECNTSerializer