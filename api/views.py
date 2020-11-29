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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

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
   
    # @action(methods=['get'], detail=False, url_path='alertas/(?P<dni>[^/.]+)')
    # def get_alertas_by_dni(self, request, dni):
    #     paciente = get_object_or_404(self.queryset, user__dni=dni)
    #     alertas = []        
    #     for acdiabetes in paciente.autocontroles_diabetes:
    #         if(acdiabetes.alerta != None):
    #             alertas.append(acdiabetes.alerta) 
 
    #     data = AlertaACDiabetes(alertas, many=True).data
    #     return Response(data, status=status.HTTP_200_OK)

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

class AlertaACDiabetesViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = AlertaACDiabetes.objects.all()
    serializer_class = AlertaACDiabetesSerializer
    #permission_classes = (IsAuthenticated,)

    @action(methods=['get'], detail=False, url_path='pacientes/(?P<id>[^/.]+)')
    def get_alertas_by_paciente_id(self, request, id):
        paciente =  get_object_or_404(Paciente.objects.all(), id=id)

        pacienteData = PacienteSerializer(paciente, context={'request':request}).data
        serializer_paciente = PacienteSerializer(data=pacienteData)
        serializer_paciente.is_valid()
        acData = serializer_paciente.data['autocontrol_diabetes']
        
        alertasPaciente = []

        alertas = AlertaACDiabetes.objects.all()
        serializer_alerta = AlertaACDiabetesSerializer(data=alertas)
        serializer_alerta.is_valid()
        alertasData = serializer_alerta.data

        for alerta in alertas:
            serializer_alerta = AlertaACDiabetesSerializer(alerta)
            for ac in acData:
                idACDiabetes = {"id": ac["id"]}
                idAlertaACDiabetes = {"id": serializer_alerta.data["autocontrol_diabetes_id"]}
                if(idAlertaACDiabetes['id'] == idACDiabetes['id']):
                    alertasPaciente.append(serializer_alerta.data) 
                
        return Response(alertasPaciente, status=status.HTTP_200_OK)


class ACDiabetesViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ACDiabetes.objects.all()
    serializer_class = ACDiabetesSerializer

    def create(self, request):
        data = request.data
        try:
            paciente = Paciente.objects.get(pk=data['paciente_id'])
        except Paciente.DoesNotExist():
            raise NotFound('Paciente {} no existe.'.format(paciente_id))
        serializer = ACDiabetesSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        acdiabetes = serializer.save(paciente_id=paciente.id)
        self.perform_create(serializer)
        return Response(acdiabetes, status=status.HTTP_201_CREATED)


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