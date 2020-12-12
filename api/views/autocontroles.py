from rest_framework import viewsets, mixins, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from api.models import ACDiabetes, Paciente
from api.serializers import ACDiabetesSerializer

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
        paciente.ultimo_autocontrol = acdiabetes.fecha_hora_registro
        paciente.save()
        self.perform_create(serializer)
        return Response(ACDiabetesSerializer(acdiabetes).data, status=status.HTTP_201_CREATED)