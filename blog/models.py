from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.templatetags.static import static


class Post(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    subtitulo = models.CharField(max_length=250, blank=True, verbose_name="Subtítulo")
    contenido = models.TextField(verbose_name="Contenido")
    imagen = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name="Imagen destacada")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="Autor")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de publicación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última modificación")

    class Meta:
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    @property
    def imagen_url(self):
        """Devuelve la URL de la imagen si existe, o un placeholder seguro si no."""
        if self.imagen and hasattr(self.imagen, 'url'):
            try:
                return self.imagen.url
            except Exception:
                return static('images/post_placeholder.svg')
        return static('images/post_placeholder.svg')
