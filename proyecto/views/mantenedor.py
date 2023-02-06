from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import View,TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from proyecto.auth import RoyalGuard
from function import JsonGenericView
from function import validar_rut
# models
from django.contrib.auth.models import User
from proyecto.models import Perfil
from proyecto.models import PerfilUsuario
from proyecto.models import Seccion,DocenteSeccion,AlumnoSeccion
from proyecto.models import Fase
# forms
from proyecto.content import UsuarioModelForm
from proyecto.content import SeccionModelForm
from proyecto.content import FaseModelForm

""" inicio bloque usuario"""
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
                    'perfil': perfil_usuario.perfiles,
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
    template_name = 'mantenedor/usuario/content_crear.html'

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
    model = User
    form_class = UsuarioModelForm
    template_name = 'mantenedor/usuario/content_actualizar.html'

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

class BuscadorUsuario(View):
    def post(self,request):
        list_personas = []
        if request.POST.get('parametro') == 'rut':
            rut =request.POST.get('rut','').replace('.','').replace('-','')
            usuarios = User.objects.filter(username__icontains=rut).exclude(is_superuser=True)
        if request.POST.get('perfil')  == 'profesor':
            usuarios = usuarios.filter(perfil_usuario_usuario__perfil__nombre='PROFESOR')
        if  request.POST.get('perfil') == 'alumno':
            usuarios = usuarios.filter(perfil_usuario_usuario__perfil__nombre='ALUMNO')
        for usuario in usuarios:
            text = f"{validar_rut.format_rut_without_dots(usuario.username.split('@')[0])} - {usuario.get_full_name()}"
            list_personas.append({
                'id': usuario.id, 
                'text': text
            })
        response = {
            'items': list_personas
        }
        return JsonResponse(response)

""" fin bloque usuario"""

""" inicio bloque seccion"""

class MantenedorSeccion(RoyalGuard, ListView):
    template_name = 'mantenedor/seccion/index.html'
    paginate_by = 10
    model = Seccion
    ordering = ['-fecha_desde__year','semestre_id','codigo']

class CrearSeccion(JsonGenericView, CreateView):
    model = Seccion
    form_class = SeccionModelForm
    template_name = 'mantenedor/seccion/content_crear.html'

class ActualizarSeccion(JsonGenericView, UpdateView):
    model = Seccion
    form_class = SeccionModelForm
    template_name = 'mantenedor/seccion/content_actualizar.html'

def eliminar_seccion(request,pk):
    Seccion.objects.filter(pk=pk).delete()
    return JsonResponse({
        'estado': '0',
        'respuesta': 'Sección eliminada con exito!'
    }, status=200,safe=False)

class AdministrarSeccion(TemplateView):
    template_name='mantenedor/seccion/content_administrar.html'

    def post(self,request,pk,metodo,perfil,usuario=None):
        if metodo == 'asignar':
            if usuario:
                if perfil == 'profesor':
                    if not DocenteSeccion.objects.filter(usuario_id = usuario,seccion = pk).exists():
                        DocenteSeccion.objects.create(
                            usuario_id = usuario,
                            seccion_id = pk,
                            responsable = request.user
                        )
                    else:
                        DocenteSeccion.objects.filter(seccion = pk).update(
                            usuario_id = usuario,
                            responsable = request.user
                        )
                    return JsonResponse({
                        'estado': '0',
                        'respuesta': 'Profesor asignado con exito!'
                    }, status=200,safe=False)
                else:
                    if not AlumnoSeccion.objects.filter(usuario_id = usuario,seccion = pk).exists():
                        AlumnoSeccion.objects.create(
                            usuario_id = usuario,
                            seccion_id = pk,
                            responsable = request.user
                        )
                        return JsonResponse({
                            'estado': '0',
                            'respuesta': 'Alumno asignado con exito!'
                        }, status=200,safe=False)
                    else:
                        return JsonResponse({
                            'estado': '0',
                            'respuesta': 'Alumno ya existe!'
                        }, status=400,safe=False)
            else:
                return JsonResponse({
                    'estado': '0',
                    'respuesta': 'El usuario es un campo obligatorio!'
                }, status=400,safe=False)

        elif metodo == 'eliminar':

            if perfil == 'profesor':
                DocenteSeccion.objects.filter(usuario_id = usuario,seccion = pk).delete()
            else:
                AlumnoSeccion.objects.filter(usuario_id = usuario,seccion = pk).delete()
            return JsonResponse({
                'estado': '0',
                'respuesta': f"El {perfil} fue quitado de la sección con exito",
                'seccion':pk,
                'perfil':perfil,
            }, status=200,safe=False)
        else:
            if perfil == 'profesor':
                lista = DocenteSeccion.objects.filter(seccion = pk)
            else:
                print(perfil)
                lista = AlumnoSeccion.objects.filter(seccion = pk)
                print(lista)
            data = []
            for usuario in lista:
                rut = usuario.usuario.username.split('@')[0]
                data.append({
                    'rut': validar_rut.format_rut_without_dots(rut),
                    'nombre_completo': usuario.usuario.get_full_name(),
                    'btn_eliminar_usuario_seccion': f"<i class='bx bx-x text-danger clickeable btn_eliminar_usuario_seccion' seccion='/mantenedor/seccion/{pk}/eliminar/{perfil}/{usuario.usuario.id}/'></i>"
                })
            response = {
                'data': data
            }
            return JsonResponse(response)

""" fin bloque seccion"""

""" inicio bloque fase"""

class MantenedorFase(RoyalGuard, ListView):
    template_name = 'mantenedor/fase/index.html'
    paginate_by = 10
    model = Fase
    ordering = ['nombre']

class CrearFase(JsonGenericView, CreateView):
    model = Fase
    form_class = FaseModelForm
    template_name = 'mantenedor/fase/content_crear.html'

class ActualizarFase(JsonGenericView, UpdateView):
    model = Fase
    form_class = FaseModelForm
    template_name = 'mantenedor/fase/content_actualizar.html'

def eliminar_fase(request,pk):
    Fase.objects.filter(pk=pk).delete()
    return JsonResponse({
        'estado': '0',
        'respuesta': 'Fase eliminada con exito!'
    }, status=200,safe=False)

""" fin bloque fase"""




def mantenedor_fases(request):
    return render(request, "mantenedor/fases/index.html")         

def mantenedor_proyecto(request):
    return render(request, "mantenedor/proyecto/index.html")      

def lista_secciones(request):
    return render(request, "seccion/lista_secciones.html")       

def lista_alumnos(request):
    return render(request, "seccion/lista_alumnos.html")    

def mantenedor_actividades(request):
    return render(request, "mantenedor/actividad/index.html")  

def mantenedor_configuracionBase(request):

    return render(request, "mantenedor/configuracionBase/index.html")         
