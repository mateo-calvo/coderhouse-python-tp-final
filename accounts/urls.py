from django.urls import path
from .views import (
    RegistroView,
    CustomLoginView,
    CustomLogoutView,
    MiPerfilView,
    EditarPerfilView,
    CustomPasswordChangeView
)

urlpatterns = [
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('perfil/', MiPerfilView.as_view(), name='mi_perfil'),
    path('perfil/editar/', EditarPerfilView.as_view(), name='editar_perfil'),
    path('perfil/password/', CustomPasswordChangeView.as_view(), name='cambiar_password'),
]
