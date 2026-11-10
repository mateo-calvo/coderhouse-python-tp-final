from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post
from accounts.models import Perfil


class Command(BaseCommand):
    help = 'Puebla la base de datos con un superusuario, usuarios y publicaciones de prueba.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Iniciando carga de datos de demostración...'))

        # Crear o actualizar superusuario
        admin_user, admin_created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@coderblog.com',
                'first_name': 'Administrador',
                'last_name': 'Principal',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if admin_created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Superusuario "admin" creado (contraseña: admin123).'))
        else:
            self.stdout.write('Superusuario "admin" ya existía.')

        # Crear o actualizar usuario autor Mateo Calvo
        mateo_user, mateo_created = User.objects.get_or_create(
            username='mateo',
            defaults={
                'email': 'mateocalvo1706@gmail.com',
                'first_name': 'Mateo',
                'last_name': 'Calvo',
            }
        )
        if mateo_created:
            mateo_user.set_password('coder123')
            mateo_user.save()
            perfil, _ = Perfil.objects.get_or_create(user=mateo_user)
            perfil.bio = "Desarrollador Python y entusiasta del desarrollo web. Estudiante en Coderhouse."
            perfil.sitio_web = "https://github.com/mateo-calvo"
            perfil.save()
            self.stdout.write(self.style.SUCCESS('Usuario autor "mateo" creado (contraseña: coder123).'))
        else:
            self.stdout.write('Usuario "mateo" ya existía.')

        # Publicaciones de demostración
        posts_data = [
            {
                'titulo': 'Dominando Django: La Guía Definitiva del Framework Web',
                'subtitulo': 'Cómo construir aplicaciones web robustas, escalables y seguras desde cero con Python.',
                'contenido': (
                    'Django es un framework web de alto nivel basado en Python que fomenta un desarrollo rápido '
                    'y un diseño limpio y pragmático.\n\n'
                    'Construido por desarrolladores experimentados, se encarga de gran parte de la molestia del '
                    'desarrollo web, para que puedas concentrarte en escribir tu aplicación sin necesidad de reinventar la rueda.\n\n'
                    'En este artículo exploramos cómo el patrón MVT (Modelo-Vista-Template), el ORM integrado y las '
                    'Class-Based Views permiten estructurar proyectos escalables con un mínimo de código boilerplate.'
                ),
                'autor': mateo_user,
            },
            {
                'titulo': 'Autenticación y Seguridad en Django para Principiantes',
                'subtitulo': 'Protegiendo vistas, gestionando contraseñas seguras y controlando accesos de usuarios.',
                'contenido': (
                    'La seguridad no debería ser una ocurrencia tardía en el desarrollo de software. '
                    'Afortunadamente, Django incluye un sistema de autenticación completo y robusto.\n\n'
                    'Mediante el uso de decoradores como @login_required o mixins como LoginRequiredMixin y '
                    'UserPassesTestMixin, podemos garantizar que rutas sensibles para la creación, modificación '
                    'o eliminación de recursos nunca queden expuestas a usuarios anónimos o no autorizados.\n\n'
                    'Además, el hashing seguro de claves mediante PBKDF2 y la protección automática contra ataques '
                    'CSRF convierten a Django en un entorno sumamente seguro por defecto.'
                ),
                'autor': mateo_user,
            },
            {
                'titulo': 'Manejo Eficiente de Archivos Estáticos y Media en Entornos de Desarrollo',
                'subtitulo': 'Configurando MEDIA_URL, MEDIA_ROOT y protegiendo los templates contra imágenes inexistentes.',
                'contenido': (
                    'Una de las dudas más frecuentes en proyectos web es la diferencia fundamental entre archivos '
                    'estáticos (CSS, JS, imágenes de diseño) y archivos media (imágenes o documentos subidos por los usuarios).\n\n'
                    'En settings.py es fundamental configurar correctamente MEDIA_ROOT y MEDIA_URL, y en urls.py '
                    'vincularlos cuando DEBUG esté en True.\n\n'
                    'Asimismo, es una buena práctica de ingeniería defensiva asegurar que los templates cuenten con '
                    'comprobaciones condicionales o fallbacks para que la aplicación nunca lance un error 500 en caso '
                    'de que un usuario publique un artículo sin imagen.'
                ),
                'autor': admin_user,
            },
            {
                'titulo': 'Patrón MVT vs MVC: Entendiendo la Arquitectura de Django',
                'subtitulo': 'Desmitificando cómo fluyen las peticiones HTTP a través del router, las vistas y los modelos.',
                'contenido': (
                    'A menudo se compara la arquitectura de Django con el clásico MVC (Modelo-Vista-Controlador). '
                    'Sin embargo, Django implementa lo que se denomina MVT: Modelo, Vista y Template.\n\n'
                    'En esta arquitectura, el propio framework Django actúa como el Controlador principal, encargándose '
                    'del enrutamiento de URLs hacia las vistas correspondientes, mientras que la Vista se enfoca en la '
                    'lógica de negocio y el Template en la presentación visual renderizada hacia el cliente.'
                ),
                'autor': mateo_user,
            },
        ]

        posts_creados = 0
        for data in posts_data:
            post, created = Post.objects.get_or_create(
                titulo=data['titulo'],
                defaults=data
            )
            if created:
                posts_creados += 1

        self.stdout.write(self.style.SUCCESS(f'Carga completada: {posts_creados} publicaciones nuevas creadas.'))
