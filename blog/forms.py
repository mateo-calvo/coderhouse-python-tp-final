from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('titulo', 'subtitulo', 'contenido', 'imagen')
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Mis primeros pasos en Django y Python'
            }),
            'subtitulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Breve resumen o subtítulo atrapante'
            }),
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Escribe aquí el contenido completo de tu publicación...'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
