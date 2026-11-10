from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Perfil


class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='mateo_test',
            email='mateo@test.com',
            password='TestPassword123!',
            first_name='Mateo',
            last_name='Calvo'
        )

    def test_perfil_creado_automaticamente(self):
        """Verifica que el perfil con avatar/bio se cree automáticamente via post_save signal."""
        self.assertTrue(hasattr(self.user, 'perfil'))
        self.assertEqual(self.user.perfil.user, self.user)

    def test_login_exitoso(self):
        """Prueba el inicio de sesión correcto de un usuario."""
        response = self.client.post(reverse('login'), {
            'username': 'mateo_test',
            'password': 'TestPassword123!'
        })
        self.assertRedirects(response, reverse('post_list'))

    def test_logout_exitoso(self):
        """Prueba el cierre de sesión."""
        self.client.login(username='mateo_test', password='TestPassword123!')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('post_list'))

    def test_ruta_perfil_protegida_para_anonimos(self):
        """Un usuario no autenticado no debe poder acceder a mi_perfil ni editar_perfil."""
        response_perfil = self.client.get(reverse('mi_perfil'))
        self.assertEqual(response_perfil.status_code, 302)
        self.assertIn(reverse('login'), response_perfil.url)

        response_editar = self.client.get(reverse('editar_perfil'))
        self.assertEqual(response_editar.status_code, 302)
        self.assertIn(reverse('login'), response_editar.url)

    def test_edicion_perfil_autenticado(self):
        """Un usuario autenticado puede actualizar su biografía y datos."""
        self.client.login(username='mateo_test', password='TestPassword123!')
        response = self.client.post(reverse('editar_perfil'), {
            'first_name': 'Mateo',
            'last_name': 'Calvo Actualizado',
            'email': 'mateo_actualizado@test.com',
            'bio': 'Nueva biografía de prueba',
            'sitio_web': 'https://github.com/mateo-calvo'
        })
        self.assertRedirects(response, reverse('mi_perfil'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, 'Calvo Actualizado')
        self.assertEqual(self.user.perfil.bio, 'Nueva biografía de prueba')
