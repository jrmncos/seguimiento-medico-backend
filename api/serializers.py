from rest_framework import serializers

from .models import User, ECNT, Paciente


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['user', 'ecnts']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['dni','first_name', 'last_name', 'password', 'location', 'bod', 'latitude', 'longitude']

class ECNTSerializer(serializers.ModelSerializer):
    pacientes = PacienteSerializer(many=True, read_only=True)
    class Meta:
        model = ECNT
        fields = ['nombre', 'descripcion', 'pacientes']
