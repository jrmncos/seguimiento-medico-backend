from rest_framework import viewsets, mixins, generics, permissions

from api.models import Group
from api.serializers import GroupSerializer

class GroupViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer