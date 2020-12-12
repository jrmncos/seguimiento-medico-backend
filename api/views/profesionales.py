from rest_framework import viewsets, mixins, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from api.models import ProfesionalDeSalud, Paciente
from api.serializers import ProfesionalDeSaludSerializer, PacienteSerializer

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