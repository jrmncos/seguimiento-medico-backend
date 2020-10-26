import pytest
import json

from api.models import User
from api.serializers import UserSerializer
from api.views import UserViewSet
from django.urls import reverse
from django_mock_queries.query import MockSet
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
class CreateUserTest(APITestCase):
    def test_create_account(self):
            userJson = {"dni":"23649864","first_name":"Germán","last_name":"Tres","latitude":-34.558772763400,"longitude":-58.744836766200,"bod":"1990-05-05","password":"cosri8773","paciente_profile":{"ultimo_autocontrol":"hoy","ecnts":[{"nombre":"diabetes","descripcion":"nivel de glucemia elevado"}]}}
            url = reverse('user-list')
            response = self.client.post(url, userJson, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(User.objects.count(), 1)
            self.assertEqual(User.objects.get().first_name, 'Germán')

class TestUserSerializer:

    def test_expected_serializer(self):      

        expected_results = {
            'id': 1,
            'dni': 38693022,
            'first_name': 'Barbara',
            'last_name': 'Saucedo',
            'bod': '1995-03-01',
            'latitude': '-34.498704674600', 
            'longitude':'-58.727045648900'
        }       

        user = User(**expected_results)

        results = UserSerializer(user).data

        assert results == expected_results


class TestUserViewSet:

    @pytest.mark.urls('api.urls')
    def test_list(self, rf, mocker):
        url = reverse('user-list')
        request = rf.get(url)

        queryset = MockSet(
            User(email = "santiagodgalvan@gmail.com",
                first_name = "Santiago",
                last_name = "Galvan",
                bod = "1995-01-05",
                dni = 38692907,
                latitude = -34.500728717200,
                longitude = -58.725495777400),
            User(email = "gercos@gmail.com",
                first_name = "Costilla",
                last_name = "German",
                bod = "1998-02-04",
                dni = 40263952,
                latitude = -34.541521068900, 
                longitude =  -58.713934007600)
        )

        mocker.patch.object(UserViewSet, 'get_queryset', return_value=queryset)
        response = UserViewSet.as_view({'get': 'list'})(request).render()

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 2