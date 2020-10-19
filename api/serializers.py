from rest_framework import serializers

from .models import User, ECNT, Paciente

# {FORM1 + FORM2 + FORM3}

class ECNTSerializer(serializers.ModelSerializer):
    class Meta:
        model = ECNT
        fields = ['nombre', 'descripcion']

#HyperlinkModelSerializer para ver el campo realted como una url

class PacienteSerializer(serializers.ModelSerializer):
    ecnts =  ECNTSerializer(read_only= True,many=True)
    class Meta:
        model = Paciente
        fields = ['ultimo_autocontrol', 'ecnts']



class UserSerializer(serializers.ModelSerializer):
    paciente_profile = PacienteSerializer()
    class Meta:
        model = User
        fields = ['dni','first_name', 'last_name', 'password', 'bod', 'latitude', 'longitude', 'paciente_profile']
        

    def create(self, validated_data):
        paciente_profile = validated_data.pop('paciente_profile')
        user = User.objects.create(**validated_data)
        print(paciente_profile)
        Paciente.objects.create(user=user, **paciente_profile)
        return user

    def update(self, instance, validated_data):
        paciente_profile = validated_data.pop('paciente_profile')
        #Chequear aca, si el profile es null vas a pisar la bd
        #... validaciones
        
        paciente = instance.paciente_profile

        #Si quisiera cambiar el dni
        #instance.dni = validated_data.get('dni', instance.dni)
        #Solo voy a permitir cambiar la location o fecha de nacimiento
        instance.bod = validated_data.get('bod', instance.bod)
        instance.save()

        paciente = paciente_profile.get('ultimo_autocontrol', profile.ultimo_autocontrol)
        paciente = paciente_profile.get('ecnts', profile.ecnts)
        profile.save()

        return instance