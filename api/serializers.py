from rest_framework import serializers

from .models import User, ECNT, Paciente, AutocontrolDiabetes

# {FORM1 + FORM2 + FORM3}

"""
class AutocontrolDiabetesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutocontrolDiabetes
        fields= '__all__'

class ECNTSerializer(serializers.ModelSerializer):
    class Meta:
        model = ECNT
        fields = ['nombre', 'descripcion']
"""

#HyperlinkModelSerializer para ver el campo realted como una url


class UserSerializer(serializers.ModelSerializer):
    """
    Ejemplo para validar un field
    def validate_password(self, value):
        if value.isalnum():
            raise serializers.ValidationError('password must have atleast one special character.')
        return value
    """
    """
    Con este metodo puedo pre-procesar el diccionario que viene del frontend
    def to_internal_value(self, data):
        user_data = data['user']
        return super().to_internal_value(user_data)
        {'dni' : 40861249 }
    """
    def validate(self, data):
        if data['first_name'] == data['last_name']:
            raise serializers.ValidationError("first_name and last_name shouldn't be same.")
        return data

    class Meta:
        model = User
        fields = ['id','dni','first_name', 'last_name', 'password', 'bod', 'latitude', 'longitude']
        #Implicitamente se valida todo lo del model + el id va solo en la serializacion y la pass en la deserializacion
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }
    
    """
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    """
class ECNTSerializer(serializers.ModelSerializer):
    class Meta:
        model = ECNT
        fields = ['id','nombre', 'descripcion']
        

class PacienteSerializer(serializers.ModelSerializer):
    ecnts =  ECNTSerializer(many=True, required=True)
    user = UserSerializer(required=True)
    
    class Meta:
        model = Paciente
        fields = ['id','ultimo_autocontrol', 'ecnts', 'user']
        read_only_fields = ('id')
    
