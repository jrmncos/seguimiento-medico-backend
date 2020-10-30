from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, generics
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser 
from .models import User, ECNT, Paciente, AutocontrolDiabetes
from .serializers import UserSerializer, PacienteSerializer, ECNTSerializer, ACDiabetesSerializer
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .services import AutocontrolDiabetesService

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

    @action(methods=['get'], detail=True)
    def get_paciente_id(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        paciente_id = user.paciente_profile.id
        print(paciente_id)
        return Response({'id':paciente_id})
        
class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all() 
    serializer_class = PacienteSerializer

class ECNTViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ECNT.objects.all()
    serializer_class = ECNTSerializer
    permission_classes = (IsAuthenticated,)

class AutocontrolDiabetesViewSet(viewsets.ModelViewSet):
    queryset = AutocontrolDiabetes.objects.all()
    serializer_class = ACDiabetesSerializer

    def perform_create(self, serializer):
        autocontrol_service = AutocontrolDiabetesService()
        autocontrol_service.check_autocontrol(serializer.validated_data)
        
        super().perform_create(serializer)

class NotificacionView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializer = NotificacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)