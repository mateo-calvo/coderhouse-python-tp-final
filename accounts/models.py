from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    avatar = models.ImageField(upload_to='avatares/', blank=True, null=True, verbose_name="Imagen de perfil")
    bio = models.TextField(max_length=500, blank=True, default="", verbose_name="Biografía")
    sitio_web = models.URLField(max_length=200, blank=True, default="", verbose_name="Sitio web o red social")

    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuarios"

    def __str__(self):
        return f"Perfil de {self.user.username}"

    @property
    def avatar_url(self):
        """Devuelve la URL del avatar o una imagen por defecto si no tiene."""
        if self.avatar and hasattr(self.avatar, 'url'):
            try:
                return self.avatar.url
            except Exception:
                return static('images/default_avatar.svg')
        return static('images/default_avatar.svg')


@receiver(post_save, sender=User)
def crear_o_guardar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
    else:
        # Si el usuario ya existía sin perfil, lo aseguramos
        if hasattr(instance, 'perfil'):
            instance.perfil.save()
        else:
            Perfil.objects.create(user=instance)
