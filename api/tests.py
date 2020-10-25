
import datetime
import json
from time import strftime

import pytest
from django.urls import reverse
from django_mock_queries.query import MockSet
from rest_framework.exceptions import ValidationError
from rest_framework import status


from .models import User
from .serializers import UserSerializer
from .views import UserViewSet



class  UserTestAPI:

    @pytest.mark.urls('api.urls')
    def test_list(self, rf, mocker):
        assert 1 == 1

    """
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
        userJson = {"dni":"23649864","first_name":"Germán","last_name":"Tres","latitude":-34.55877276343772,"longitude":-58.74483676627278,"bod":"1990-05-05","password":"cosri8773","paciente_profile":{"ultimo_autocontrol":"hoy","ecnts":[{"nombre":"diabetes","descripcion":"nivel de glucemia elevado"}]}}
        
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