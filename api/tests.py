from django.test import TestCase

from .models import User, Paciente
from .serializers import PacienteSerializer, UserSerializer
from datetime import date

from rest_framework.test import APITestCase, APIClient
from django.urls import reverse


# Create your tests here.
class PacienteTest(TestCase):

    def test_user_model_has_profile(self):
        user = User(
            dni='40861249',
            password='abc1cba'
        )
        user.save()

        self.assertTrue(
            hasattr(user,'paciente_profile')
        )
"""
class PacienteManager:

    def test_get_pacientes_by_ecnt(self, mocker):

        expected_results = [
            Paciente()
        ]

        ecnt = 'diabetes'
        qs = MockSet(expected_results[0])

        mocker.patch.object(Paciente.objects, 'get_queryset', return_value=qs)

        result = list(Car.objects.paciente_by_ecnt(ecnt))

        assert result == expected_results
        assert str(result[0]) == expected_results[0].code


class TestPacienteSerializer(TestCase):

    def test_expected_serialized_json(self):
        
        expected_results = {
            'user': User(dni="40861249",
             first_name="German",
             last_name="Costilla",
             password="abc1cba",
             latitude=53.05623,
             longitude=5.5653,
             bod=date.today()),
             'ultimo_autocontrol': 'ayer'
        }

        paciente = Paciente(**expected_results)
        print(paciente)
        result = PacienteSerializer(paciente).data
        print(result)
        assert result == expected_results


class BasePacienteTest(APITestCase):
    client = APIClient()

   
    def setUp(self):
        #Mockeo DB
        user1 = User(dni="4482361249",
             first_name="German",
             last_name="Costilla",
             password="abc1cba",
             latitude=53.05623,
             longitude=5.5653,
             bod=date.today())
        user1.save()

        user2 = User(dni="4386165249",
             first_name="German",
             last_name="Costilla",
             password="abc1cba",
             latitude=53.05623,
             longitude=5.5653,
             bod=date.today())
        user2.save()
   
        
class PacienteTestAPI(BasePacienteTest):
    
    def test_get_all_pacientes(self):

        expected = Paciente.objects.all()
        serialized = PacienteSerializer(expected, many=True)
        
        response = self.client.get(
            '/api/pacientes/'
        )
        
        self.assertEqual(response.data, serialized.data)
   
    def test_put_paciente(self):
        json = {
            'first_name': 'German',
            'last_name': 'Costilla',
            'dni': '40861249',
            'bod': '05/05/1990',
            'latitude': '35.0653',
            'longitude': '35.0653',
            'password':'abc1cba',
            'paciente_profile': {
                'ultimo_autocontrol': 'hoy',
                'ectns': []
            }  
        }
        
        response = self.client.put(
            '/api/pacientes/',
            json,
            format='json'
        )

        self.assertEqual(len(Paciente.objects.all()), 2)



class UserSerializer(TestCase):
    expected_results = {
            'first_name': 'German',
            'last_name': 'Costilla',
            'dni': '40861249',
            'bod': '05/05/1990',
            'latitude': '35.0653',
            'longitude': '35.0653',
            'password':'abc1cba',
            'paciente_profile': {
                'ultimo_autocontrol': 'hoy'
            }
    }

    serializer = UserSerializer(expected_results)
    print(serializer.data)
    print(serializer)

"""


class BasePacienteTest(APITestCase):
    client = APIClient()

    def setUp(self):
        user1 = User(dni="4482361249",
             first_name="German",
             last_name="Costilla",
             password="abc1cba",
             latitude=53.05623,
             longitude=5.5653,
             bod=date.today())
        user1.save()

        user2 = User(dni="4386165249",
             first_name="German",
             last_name="Costilla",
             password="abc1cba",
             latitude=53.05623,
             longitude=5.5653,
             bod=date.today())
        user2.save()
   
        
class PacienteTestAPI(BasePacienteTest):
    
    def test_get_all_pacientes(self):

        expected = Paciente.objects.all()
        serialized = PacienteSerializer(expected, many=True)
        
        response = self.client.get(
            '/api/pacientes/'
        )
        
        self.assertEqual(response.data, serialized.data)
   
    def test_put_paciente(self):


        data = {
            "dni": 76532565,
            "first_name": "gerr",
            "last_name": "costtt",
            "password": "costi8773",
            "bod": "2020-10-18",
            "latitude": "53.3235000000000000",
            "longitude": "26.2356000000000000",
            "paciente_profile": {
                "ultimo_autocontrol": "Hola"
            }
        }
        response = self.client.put(
            '/api/users/',
            data,
            format='json'
        )

        serialize = UserSerializer(data=data)
        print("RESP")
        print(serialize.is_valid())

        self.assertEqual(len(Paciente.objects.all()), 3)