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
from django.test import TestCase

"""
Al crear un user se crea un paciente
"""
class Integration(TestCase):
    def test_cli(self):
        assert True == True

"""
class UserProfileTest(TestCase):
    def test_user_model_has_profile(self):
        user = User(email = "santiagodgalvan@gmail.com",
                first_name = "Santiago",
                last_name = "Galvan",
                bod = "1995-01-05",
                dni = 38692907,
                latitude = -34.500728717200,
                longitude = -58.725495777400)
        user.save()

        self.assertTrue(hasattr(user, 'paciente_profile'))


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
        print(rf)
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

    @pytest.mark.urls('api.urls')
    def test_get_user_by_dni(self, rf, mocker):
        url = reverse('user-list')
        print(rf)
        request = rf.get(url+"/dni/38692907")

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
        assert len(json.loads(response.content)).get('dni') == 38692907
    
    @pytest.mark.urls('api.urls')
    @pytest.mark.django_db
    def test_create(self, rf, mocker):
        url = reverse('user-list')

        data = {
            "dni":"23649864",
            "first_name":"Germán",
            "last_name":"Tres",
            "latitude":-34.558772763400,
            "longitude":-58.744836766200,
            "bod":"1990-05-05",
            "password":"costi8773"
        }

        request = rf.post(url, content_type='application/json', data=json.dumps(data))
        #Mock el object posta pero
        #podes ver lo que hace
        mocker.patch.object(User, 'save')
        response = UserViewSet.as_view({'post':'create'})(request).render()

        assert response.status_code == 201
        assert json.loads(response.content).get('dni') == 23649864
        assert User.save.called

    @pytest.mark.urls('api.urls')
    @pytest.mark.django_db
    def test_update(self, rf, mocker):
        url = reverse('user-detail', kwargs={'pk':1})
        request = rf.patch(url, content_type='application/json', data = json.dumps({'first_name':'Damian'}))
        
        user = User(id = 1,   
                    email = "santiagodgalvan@gmail.com",
                    first_name = "Santiago",
                    last_name = "Galvan",
                    bod = "1995-01-05",
                    dni = 38692907,
                    latitude = -34.500728717200,
                    longitude = -58.725495777400)

        mocker.patch.object(UserViewSet, 'get_object', return_value=user)
        mocker.patch.object(User, 'save')

        response = UserViewSet.as_view({'patch': 'partial_update'})(request).render()
        assert response.status_code == 200
        assert json.loads(response.content).get('first_name') == 'Damian'
        assert User.save.called

  
    @pytest.mark.urls('garage.urls')
    def test_delete(self, rf, mocker):
        url = reverse('car-detail', kwargs={'pk': 1})
        request = rf.delete(url)

        car = Car(name='Ferrari',
                  code='fr1',
                  id=1,
                  year=2019,
                  created=datetime.datetime.now(),
                  modified=datetime.datetime.now())

        # De nuevo hacemos patch al metodo get_object
        # y tambien al delete del objeto.
        mocker.patch.object(CarViewSet, 'get_object', return_value=car)
        mocker.patch.object(Car, 'delete')

        response = CarViewSet \
            .as_view({'delete': 'destroy'})(request).render()

        assert response.status_code == 204
        assert Car.delete.called

    """