from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post


class BlogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='autor1',
            email='autor1@test.com',
            password='TestPassword123!'
        )
        self.user2 = User.objects.create_user(
            username='autor2',
            email='autor2@test.com',
            password='TestPassword123!'
        )
        self.post1 = Post.objects.create(
            titulo='Aprender Django desde Cero',
            subtitulo='Una guía completa',
            contenido='Contenido detallado de prueba sobre Django...',
            autor=self.user1
        )

    def test_listado_publico_para_visitante_anonimo(self):
        """Cualquier visitante anónimo puede ver el listado de posts."""
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aprender Django desde Cero')

    def test_detalle_publico_para_visitante_anonimo(self):
        """Cualquier visitante anónimo puede ver el detalle de un post."""
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contenido detallado de prueba sobre Django...')

    def test_creacion_post_requiere_login(self):
        """Un usuario anónimo debe ser redirigido a login al intentar crear un post."""
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_creacion_post_autenticado(self):
        """Un usuario autenticado puede crear un post correctamente."""
        self.client.login(username='autor1', password='TestPassword123!')
        response = self.client.post(reverse('post_create'), {
            'titulo': 'Nuevo Post de Coderhouse',
            'subtitulo': 'Subtítulo interesante',
            'contenido': 'Contenido del nuevo post'
        })
        self.assertEqual(response.status_code, 302)
        nuevo_post = Post.objects.get(titulo='Nuevo Post de Coderhouse')
        self.assertEqual(nuevo_post.autor, self.user1)

    def test_solo_autor_puede_editar_post(self):
        """El autor puede editar su propio post, pero otro usuario no."""
        # Usuario 2 intenta editar el post del Usuario 1
        self.client.login(username='autor2', password='TestPassword123!')
        response_intruso = self.client.get(reverse('post_update', kwargs={'pk': self.post1.pk}))
        self.assertEqual(response_intruso.status_code, 302)

        # Usuario 1 edita su propio post
        self.client.login(username='autor1', password='TestPassword123!')
        response_autor = self.client.post(reverse('post_update', kwargs={'pk': self.post1.pk}), {
            'titulo': 'Título Modificado por el Autor',
            'subtitulo': self.post1.subtitulo,
            'contenido': self.post1.contenido,
        })
        self.assertEqual(response_autor.status_code, 302)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.titulo, 'Título Modificado por el Autor')

    def test_busqueda_de_posts(self):
        """El buscador debe filtrar correctamente por palabras clave."""
        response_encontrado = self.client.get(reverse('post_list'), {'q': 'Django'})
        self.assertEqual(response_encontrado.status_code, 200)
        self.assertContains(response_encontrado, 'Aprender Django desde Cero')

        response_no_encontrado = self.client.get(reverse('post_list'), {'q': 'ReactJSInexistente'})
        self.assertEqual(response_no_encontrado.status_code, 200)
        self.assertContains(response_no_encontrado, 'No se encontraron artículos')

    def test_post_sin_imagen_no_rompe_template(self):
        """Un post sin imagen renderiza perfectamente sin causar errores de template."""
        self.assertFalse(bool(self.post1.imagen))
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1.titulo)
