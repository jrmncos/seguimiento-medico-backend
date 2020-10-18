from django.test import TestCase

from .models import User, Paciente

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