from rest_framework import viewsets, mixins, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from api.models import User, Group, ProfesionalDeSalud
from api.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    @action(methods=['get'], detail=False, url_path='dni/(?P<dni>[^/.]+)')
    def get_user_by_dni(self, request, dni):
        user = get_object_or_404(self.queryset, dni=dni)
        data = UserSerializer(user, context={'request':request}).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(methods=['patch'], detail=True)
    def add_groups(self, request, *args, **kwargs):
        user = self.get_object()
        data = UserSerializer(user, context={'request':request}).data
        user.groups.clear()
        for grupo in request.data['groups']:
            user.groups.add(Group.objects.get(name=grupo['name'])) 
        for grupo in user.groups.all():
            print(grupo)
            if grupo.name == "Profesional de Salud" and not hasattr(user, 'profesional_profile'):
                print('arigato')
                profesional = ProfesionalDeSalud(user=user)
                profesional.save()
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
