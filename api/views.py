from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, generics
from .models import User, ECNT, Paciente
from .serializers import UserSerializer, PacienteSerializer, ECNTSerializer
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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

class ECNTViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ECNT.objects.all()
    serializer_class = ECNTSerializer
    permission_classes = (IsAuthenticated,)