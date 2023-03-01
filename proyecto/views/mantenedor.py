from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import View,TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from proyecto.auth import RoyalGuard
from function import JsonGenericView
from function import validar_rut
from django.utils import timezone
import ast
# models
from django.contrib.auth.models import User
from proyecto.models import Perfil
from proyecto.models import PerfilUsuario
from proyecto.models import Seccion,DocenteSeccion,AlumnoSeccion,Actividad,Parametro
# forms
from proyecto.content import UsuarioModelForm
from proyecto.content import SeccionModelForm


""" inicio bloque usuario"""
class MantenedorUsuario(RoyalGuard, ListView):
    template_name = 'mantenedor/usuario/index.html'
    paginate_by = 10
    model = User

    def get_queryset(self):
        filter = self.request.GET.get('filter')
        campo = self.request.GET.get('orden')
        lista_perfil_usuarios = PerfilUsuario.objects.filter(
            usuario__email__icontains='@edu.udla.cl',
        ).exclude(usuario__is_superuser=True)
        if filter:
            lista_perfil_usuarios =lista_perfil_usuarios.filter(
                Q(usuario__first_name__icontains=filter) | Q(usuario__last_name__icontains=filter) | 
                Q(usuario__username__icontains=filter) | Q(usuario__email__icontains=filter),
            )
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
        return sorted(data, key=lambda d: d[campo]) if campo else sorted(data, key=lambda d: d['rut'])

    def get_context_data(self, **kwargs):
        context = super(MantenedorUsuario, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter')
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

class CrearUsuario(RoyalGuard,JsonGenericView, CreateView):
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

class ActualizarUsuario(RoyalGuard,JsonGenericView, UpdateView):
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

class BuscadorUsuario(RoyalGuard,View):
    def post(self,request):
        list_personas = []
        if request.POST.get('parametro') == 'rut':
            rut =request.POST.get('rut','').replace('.','').replace('-','')
            usuarios = User.objects.filter(username__icontains=rut).exclude(is_superuser=True)
        if request.POST.get('perfil')  == 'profesor':
            usuarios = usuarios.filter(fk_perfil_usuario_usuario__perfil__nombre='PROFESOR')
        if  request.POST.get('perfil') == 'alumno':
            usuarios = usuarios.filter(fk_perfil_usuario_usuario__perfil__nombre='ALUMNO')
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

    def get_queryset(self):
        year_selected = int(self.request.GET.get('year')) if self.request.GET.get('year') else timezone.now().year
        lista_secciones = Seccion.objects.filter(fecha_desde__year=year_selected)
        filter = self.request.GET.get('filter')
        if filter:
            lista_secciones = lista_secciones.filter(
               Q(codigo__icontains=filter)|Q(semestre__nombre__icontains=filter)
            )
        return lista_secciones

    def get_context_data(self, **kwargs):
        context = super(MantenedorSeccion, self).get_context_data(**kwargs)
        lista_agnos = (list(Seccion.objects.all().values_list('fecha_desde__year',flat=True)) or [])
        agno_siguiente = timezone.now().year+1
        if agno_siguiente not in lista_agnos:
            lista_agnos.append(agno_siguiente)
        context['years'] = lista_agnos
        context['filter'] = self.request.GET.get('filter')
        context['year_selected'] = int(self.request.GET.get('year')) if self.request.GET.get('year') else None
        return context

class CrearSeccion(JsonGenericView, CreateView):
    model = Seccion
    form_class = SeccionModelForm
    template_name = 'mantenedor/seccion/content_crear.html'

    def form_valid(self, form):
        response = super(CrearSeccion, self).form_valid(form)
        # response_data = ast.literal_eval(response.getvalue().decode("UTF-8"))
        # if bool(response_data) and self.request.POST.get('chk_configuracion_base'):
        #     Seccion.objects.get(pk=response_data.get('id')).set_configuracion_base(self.request.user)
        return response

class ActualizarSeccion(RoyalGuard, JsonGenericView, UpdateView):
    model = Seccion
    form_class = SeccionModelForm
    template_name = 'mantenedor/seccion/content_actualizar.html'

class EliminarSeccion(RoyalGuard,DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Seccion.objects.filter(id=self.kwargs['pk'])
        return queryset
    
    def finalize_response(self, request, response, *args, **kwargs):
        return JsonResponse({
            'estado': '0',
            'respuesta': 'Sección eliminada con exito!'
        }, status=200,safe=False)

class AdministrarSeccion(RoyalGuard,TemplateView):
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
                            'estado': '2',
                            'respuesta': 'Alumno ya existe!'
                        }, status=200,safe=False)
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