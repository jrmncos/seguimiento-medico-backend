from django.test import TestCase

from .models import User, Paciente
from .serializers import PacienteSerializer, UserSerializer
from datetime import date

from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status

# Create your tests here.
"""
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
        
class  UserTestAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(
            dni=41861249, 
            password="abc1cba",
            first_name="German",
            last_name="Costilla",
            latitude=50.6896,
            longitude=76.04689,
            bod=date.today())
        cls.paciente = Paciente.objects.create(user=cls.user1, ultimo_autocontrol="Hoy")
    
    def test_get_all_users(self):
        expected = User.objects.all()
        serialized = UserSerializer(expected, many=True)
        #print(serialized.data)
        response = self.client.get(
            reverse("user-list")
        )
        self.assertEqual(response.data, serialized.data)

    def test_get_user_by_id(self):
        expected = User.objects.all().filter(pk=1)[0]
        serialized = UserSerializer(expected)
        response = self.client.get(
            reverse("user-detail", args=[self.user1.id])
        )
        self.assertEqual(response.data, serialized.data)
    
    def test_get_user_by_id_non_existent(self):
        response = self.client.get(
            reverse("user-detail", args=[87])
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_create_user(self):
        userJson = {
            'first_name': 'German',
            'last_name': 'Costilla',
            'dni': '40861249',
            'bod': '1990-10-12',
            'latitude': '35.0653',
            'longitude': '35.0653',
            'password':'abc1cba',
            'paciente_profile': {
                'ultimo_autocontrol': 'hoy',
                'ecnts': [
                    {'nombre': 'diabetes',
                    'descripcion': 'nivelGlucemia'}
                ]       
            }
        }
        
        response = self.client.post(
            reverse('user-list'), userJson, format='json'
        )
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

    def test_create_user_dni_repeat(self):
        userJson = {
            'first_name': 'German',
            'last_name': 'Costilla',
            'dni': str(self.user1.dni),
            'bod': '1990-10-12',
            'latitude': '35.0653',
            'longitude': '35.0653',
            'password':'abc1cba',
            'paciente_profile': {
                'ultimo_autocontrol': 'hoy',
                'ecnts': [
                    {'nombre': 'diabetes',
                    'descripcion': 'nivelGlucemia'}
                ]       
            }
        }
        response = self.client.post(
            reverse('user-list'), userJson, format='json'
        )
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

        
    """
    def test_put_paciente(self):
        pass
        
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
    """