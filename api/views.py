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

class PacienteECNT:
    def __init__(self, latitude, longitude, ecnts):
        self.latitude = latitude
        self.longitude = longitude
        self.ecnts = ecnts

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
    
    @action(methods=['get'], detail=False, url_path='ecnts')
    def get_pacientes_ecnts(self, request):
        pacientes = self.queryset.all()
        pacientesList = []
        for paciente in pacientes:
            pacientecnt = PacienteECNT(paciente.user.latitude, paciente.user.longitude, paciente.ecnts)
            pacientesList.append(pacientecnt)
        data = PacienteECNTSerializer(pacientesList, many=True).data
   
    @action(methods=['get'], detail=False, url_path='alertas/(?P<dni>[^/.]+)')
    def get_alertas_by_dni(self, request, dni):
        paciente = get_object_or_404(self.queryset, user__dni=dni)
        alertas = []        
        for acdiabetes in paciente.autocontroles_diabetes:
            if(acdiabetes.alerta != None):
                alertas.append(acdiabetes.alerta) 
 
        data = AlertaACDiabetes(alertas, many=True).data
        return Response(data, status=status.HTTP_200_OK)

class ProfesionalDeSaludViewSet(viewsets.ModelViewSet):
    queryset = ProfesionalDeSalud.objects.all() 
    serializer_class = ProfesionalDeSaludSerializer
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    #paciente/dni/40861249
    @action(methods=['get'], detail=False, url_path='dni/(?P<dni>[^/.]+)')
    def get_profesional_by_dni(self, request, dni):
        user = get_object_or_404(self.queryset, user__dni=dni)
        data = ProfesionalDeSaludSerializer(user, context={'request':request}).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(methods=['patch'], detail=True)
    def add_paciente_by_dni(self, request, *args, **kwargs):
        profesional = self.get_object()
        paciente = get_object_or_404(Paciente.objects.all(), user__dni=kwargs['dni'])
        profesional.pacientes.add(paciente)
        profesional.save()
        return Response(PacienteSerializer(paciente).data, status=status.HTTP_200_OK)
        #data = ProfesionalDeSaludSerializer(profesional,data={pacientes:})
    
class ECNTViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ECNT.objects.all()
    serializer_class = ECNTSerializer

class AlertaACDiabetesViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = AlertaACDiabetes.objects.all()
    serializer_class = AlertaACDiabetesSerializer
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
        notificacion = {
            "titulo": request.data.get("titulo"),
            "imagen": request.data.get("imagen")
        }
        serializer = self.get_serializer(data=notificacion)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print('Esta todo bien')
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    """
    def perform_create(self, serializer, request):
        enviador_notificaciones = NotificadorService()
        enviador_notificaciones.send_notificacion(serializer.validated_data)
        super().perform_create(serializer)
       

    @staticmethod
    def _get_users_by_filter(self, request):
        users = User.objects.all()
        print(request.data)
        return users
    """ 