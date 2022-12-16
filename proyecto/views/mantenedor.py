from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import View
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from proyecto.auth import RoyalGuard
from function import JsonGenericView
from function import validar_rut
# models
from django.contrib.auth.models import User
# forms
from proyecto.content import UsuarioModelForm
from proyecto.models import Perfil


class MantenedorUsuario(RoyalGuard,ListView):
    template_name = 'mantenedor/usuario/index.html'
    paginate_by = 10
    model = User

    def get_queryset(self):
        filter_val = self.request.GET.get('filter','17')
        usuarios = User.objects.filter(
            Q(first_name__icontains=filter_val)|Q(last_name__icontains=filter_val)|Q(username__icontains=filter_val),
            email__icontains='edu.udla.cl',id__gte=1,
        ).order_by('username')
        data = []
        for usuario in usuarios:
            rut = usuario.username.split('@')[0]
            data.append({
                'rut': validar_rut.format_rut_without_dots(rut),
                'nombre_completo':usuario.get_full_name(),
                'correo':usuario.email,
                'id':usuario.id,
            })
        return data

    def get_context_data(self, **kwargs):
        context = super(MantenedorUsuario, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter','1234')
        return context

class CrearUsuario(JsonGenericView, CreateView):
    model = User
    form_class = UsuarioModelForm
    template_name = 'mantenedor/usuario/content_crear_usuario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfiles'] = Perfil.objects.filter(ind_asignable=True).values("id", "nombre")
        return context

    def post(self, request, *args, **kwargs):
        if not request.POST._mutable:
            request.POST._mutable = True
        request.POST['responsable'] = request.user
        return super(CrearUsuario, self).post(request, *args, **kwargs)

class ActualizarUsuario(JsonGenericView, UpdateView):
    """ actualiza anexo """
    model = User
    form_class = UsuarioModelForm
    template_name = 'mantenedor/usuario/content_actualizar_usuario.html'