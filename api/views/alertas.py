from rest_framework import viewsets, mixins, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from api.models import AlertaACDiabetes
from api.serializers import AlertaACDiabetesSerializer, PacienteSerializer

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
