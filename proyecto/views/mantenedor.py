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
from proyecto.models import PerfilUsuario


class MantenedorUsuario(RoyalGuard, ListView):
    template_name = 'mantenedor/usuario/index.html'
    paginate_by = 10
    model = User

    def get_queryset(self):
        filtro = '@edu.udla.cl'
        if self.request.GET.get('filtro') is not None and self.request.GET.get('filtro') !='':
            filtro = self.request.GET.get('filtro')
        campo = 'nombre_completo'
        if self.request.GET.get('orden') is not None and self.request.GET.get('orden') !='':
            campo = self.request.GET.get('orden')
        lista_perfil_usuarios = PerfilUsuario.objects.filter(
            Q(usuario__first_name__icontains=filtro) | Q(usuario__last_name__icontains=filtro) | Q(
                usuario__username__icontains=filtro) | Q(usuario__email__icontains=filtro),
        ).exclude(usuario__is_superuser=True)
        data = []
        for perfil_usuario in lista_perfil_usuarios:
            if perfil_usuario.is_perfil_habilitado:
                rut = perfil_usuario.usuario.username.split('@')[0]
                data.append({
                    'rut': validar_rut.format_rut_without_dots(rut),
                    'nombre_completo': perfil_usuario.usuario.get_full_name(),
                    'correo': perfil_usuario.usuario.email,
                    'perfil': perfil_usuario.perfil.nombre,
                    'id': perfil_usuario.usuario.id,
                    'is_staff': perfil_usuario.usuario.is_staff,
                })
        return sorted(data, key=lambda d: d[campo])

    def get_context_data(self, **kwargs):
        context = super(MantenedorUsuario, self).get_context_data(**kwargs)
        context['filtro'] = '@edu.udla.cl'
        if self.request.GET.get('filtro') is not None and self.request.GET.get('filtro') !='':
            context['filtro'] = self.request.GET.get('filtro')
        return context

    def post(self,request):
        usuario_id = request.POST.get('usuario_id')
        estado = True if int(request.POST.get('estado')) ==1 else False
        User.objects.filter(id=usuario_id).update(is_staff=estado)
        response = {
            'estado': '0',
            'respuesta':'Usuario deshabilitado!' if estado is False else 'Usuario habilitado!'
        }  
        return JsonResponse(response)

class CrearUsuario(JsonGenericView, CreateView):
    model = User
    form_class = UsuarioModelForm
    template_name = 'mantenedor/usuario/content_crear_usuario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfiles'] = Perfil.objects.filter(
            ind_asignable=True).values("id", "nombre")
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rut'] = validar_rut.format_rut_without_dots(context.get('user').username.split('@')[0])
        perfiles = list(Perfil.objects.filter(ind_asignable=True).values("id", "nombre"))
        for perfil in perfiles:
            perfil['asignado'] = True if PerfilUsuario.objects.filter(perfil_id=perfil.get('id'),usuario=context.get('user')).last() else False
        context['perfiles'] = perfiles
        return context
    
    def post(self, request, *args, **kwargs):
        if not request.POST._mutable:
            request.POST._mutable = True
        request.POST['responsable'] = request.user
        return super(ActualizarUsuario, self).post(request, *args, **kwargs)

def mantenedor_actividades(request):
    return render(request, "mantenedor/actividad/index.html")        
