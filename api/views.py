from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, generics, permissions
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser 
from .models import *
from .serializers import *
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from .services import *

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

"""
class UserViewSet(viewsets.ViewSet):
    def list(self, request):
       queryset = User.objects.all()
       serializer = UserSerializer(queryset, many=True)
       return Response(serializer.data)
        
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST )

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    #Falta implementar
    def partial_update(self, request, *args, **kwargs):
        print('Partial update')
        print(**kwargs)
        print(request)
        print(*args)
        #queryset= User.objects.all()
        #instance = queryset.get(pk=)
        #serializer = UserSerializer(data=request.data, )
        return True
"""

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    """
    @action(methods=['get'], detail=True)
    def get_id_paciente(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        paciente_id = user.paciente_profile.id
        print(paciente_id)
        return Response({'id':paciente_id})
    """

    @action(methods=['get'], detail=False, url_path='dni/(?P<dni>[^/.]+)')
    def get_user_by_dni(self, request, dni):
        user = get_object_or_404(self.queryset, dni=dni)
        data = UserSerializer(user, context={'request':request}).data
        return Response(data, status=status.HTTP_200_OK)
        
class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all() 
    serializer_class = PacienteSerializer
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    #paciente/dni/40861249
    @action(methods=['get'], detail=False, url_path='dni/(?P<dni>[^/.]+)')
    def get_paciente_by_dni(self, request, dni):
        user = get_object_or_404(self.queryset, user__dni=dni)
        data = PacienteSerializer(user, context={'request':request}).data
        return Response(data, status=status.HTTP_200_OK)

class ProfesionalDeSaludViewSet(viewsets.ModelViewSet):
    queryset = ProfesionalDeSalud.objects.all() 
    serializer_class = ProfesionalDeSaludSerializer
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    #paciente/dni/40861249
    @action(methods=['get'], detail=False, url_path='dni/(?P<dni>[^/.]+)')
    def get_profesional_by_dni(self, request, dni):
        user = get_object_or_404(self.queryset, user__dni=dni)
        data = PacienteSerializer(user, context={'request':request}).data
        return Response(data, status=status.HTTP_200_OK)

class ECNTViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ECNT.objects.all()
    serializer_class = ECNTSerializer
    #permission_classes = (IsAuthenticated,)

class AutocontrolDiabetesViewSet(viewsets.ModelViewSet):
    queryset = AutocontrolDiabetes.objects.all()
    serializer_class = ACDiabetesSerializer

    def perform_create(self, serializer):
        autocontrol_service = AutocontrolDiabetesService()
        autocontrol_service.check_autocontrol(serializer.validated_data)
        
        super().perform_create(serializer)

#class NotificacionView(viewsets.ViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
class NotificacionView(generics.CreateAPIView, generics.ListAPIView):
    parser_classes = (MultiPartParser,)
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, request)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, request):
        enviador_notificaciones = NotificadorService()
        print(request.data)
        enviador_notificaciones.send_notificacion(serializer.validated_data, filtros)
        super().perform_create(serializer)
        