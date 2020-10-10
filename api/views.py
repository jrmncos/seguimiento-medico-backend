from django.shortcuts import render
from rest_framework import viewsets
from .models import User, ECNT, Paciente
from .serializers import UserSerializer, ECNTSerializer, PacienteSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ECNTViewSet(viewsets.ModelViewSet):
    queryset = ECNT.objects.all()
    serializer_class = ECNTSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer