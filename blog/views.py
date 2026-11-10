from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from .models import Post
from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.all().select_related('autor', 'autor__perfil')
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) |
                Q(subtitulo__icontains=query) |
                Q(contenido__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '').strip()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        messages.success(self.request, '¡Publicación creada exitosamente!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = 'Crear Publicación'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    login_url = 'login'

    def test_func(self):
        post = self.get_object()
        return post.autor == self.request.user or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para editar esta publicación.')
        return redirect('post_detail', pk=self.kwargs['pk'])

    def form_valid(self, form):
        messages.success(self.request, '¡Publicación actualizada correctamente!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = 'Editar Publicación'
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    login_url = 'login'

    def test_func(self):
        post = self.get_object()
        return post.autor == self.request.user or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para eliminar esta publicación.')
        return redirect('post_detail', pk=self.kwargs['pk'])

    def form_valid(self, form):
        messages.success(self.request, 'Publicación eliminada correctamente.')
        return super().form_valid(form)


class AboutView(TemplateView):
    template_name = 'blog/about.html'
