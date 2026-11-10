from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('fecha_creacion', 'autor')
    search_fields = ('titulo', 'subtitulo', 'contenido')
    date_hierarchy = 'fecha_creacion'
