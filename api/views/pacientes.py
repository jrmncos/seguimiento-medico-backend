from rest_framework import viewsets, mixins, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from api.models import Paciente, ECNT
from api.serializers import PacienteSerializer, PacienteECNTSerializer

class PacienteECNTDTO:
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
            pacientecnt = PacienteECNTDTO(paciente.user.latitude, paciente.user.longitude, paciente.ecnts)
            pacientesList.append(pacientecnt)
        data = PacienteECNTSerializer(pacientesList, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True)
    def add_ecnts(self, request, *args, **kwargs):
        paciente = self.get_object()
        data = PacienteSerializer(paciente, context={'request':request}).data
        paciente.ecnts.clear()
        for ecnt in request.data['ecnts']:
            paciente.ecnts.add(ECNT.objects.get(nombre=ecnt['nombre'])) 

        paciente.save()
        return Response(PacienteSerializer(paciente).data, status=status.HTTP_200_OK)
