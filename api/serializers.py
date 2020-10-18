from rest_framework import serializers

from .models import User, ECNT, Paciente

# {FORM1 + FORM2 + FORM3}

class ECNTSerializer(serializers.ModelSerializer):
    class Meta:
        model = ECNT

class PacienteSerializer(serializers.ModelSerializer):
    #user = UserSerializer(read_only=True)
    #ecnts =  ECNTSerializer(read_only=True, many=True)
    class Meta:
        model = Paciente
        fields = ['ultimo_autocontrol']

class UserSerializer(serializers.ModelSerializer):
    paciente_profile = PacienteSerializer()
    class Meta:
        model = User
        fields = ['dni','first_name', 'last_name', 'password', 'bod', 'latitude', 'longitude', 'paciente_profile']



