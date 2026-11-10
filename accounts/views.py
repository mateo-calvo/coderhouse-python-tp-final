from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, DetailView
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegistroUsuarioForm, EditarUsuarioForm, EditarPerfilForm
from .models import Perfil


class RegistroView(View):
    template_name = 'accounts/registro.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('post_list')
        form = RegistroUsuarioForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('post_list')
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido/a {user.username}! Tu cuenta ha sido creada exitosamente.')
            return redirect('post_list')
        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f'¡Bienvenido de nuevo, {form.get_user().username}!')
        return super().form_valid(form)


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'Has cerrado sesión correctamente.')
        return redirect('post_list')

    def post(self, request):
        logout(request)
        messages.info(request, 'Has cerrado sesión correctamente.')
        return redirect('post_list')


class MiPerfilView(LoginRequiredMixin, View):
    template_name = 'accounts/perfil.html'

    def get(self, request):
        # Aseguramos que el usuario tenga perfil
        perfil, _ = Perfil.objects.get_or_create(user=request.user)
        posts = request.user.posts.all().order_by('-fecha_creacion')
        return render(request, self.template_name, {'perfil': perfil, 'posts': posts})


class EditarPerfilView(LoginRequiredMixin, View):
    template_name = 'accounts/editar_perfil.html'

    def get(self, request):
        perfil, _ = Perfil.objects.get_or_create(user=request.user)
        user_form = EditarUsuarioForm(instance=request.user)
        perfil_form = EditarPerfilForm(instance=perfil)
        return render(request, self.template_name, {
            'user_form': user_form,
            'perfil_form': perfil_form,
        })

    def post(self, request):
        perfil, _ = Perfil.objects.get_or_create(user=request.user)
        user_form = EditarUsuarioForm(request.POST, instance=request.user)
        perfil_form = EditarPerfilForm(request.POST, request.FILES, instance=perfil)

        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, 'Tu perfil ha sido actualizado con éxito.')
            return redirect('mi_perfil')

        return render(request, self.template_name, {
            'user_form': user_form,
            'perfil_form': perfil_form,
        })


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/cambiar_password.html'
    success_url = reverse_lazy('mi_perfil')

    def form_valid(self, form):
        messages.success(self.request, 'Tu contraseña ha sido actualizada con éxito.')
        return super().form_valid(form)
