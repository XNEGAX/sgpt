from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from proyecto.auth import RoyalGuard
from function import JsonGenericView
from django.utils import timezone
from function import validar_rut
# models
from proyecto.models import DocenteSeccion
from proyecto.models import AlumnoSeccion
from proyecto.models import Actividad
# forms
from proyecto.content import ActividadModelForm

""" inicio bloque seccion docente"""

class MantenedorSeccionesDocente(RoyalGuard,ListView):
    template_name = 'docente/seccion/index.html'
    paginate_by = 10
    model = DocenteSeccion

    def get_queryset(self):
        year_selected = int(self.request.GET.get('year')) if self.request.GET.get('year') else timezone.now().year
        lista_secciones_docente = DocenteSeccion.objects.filter(
            usuario=self.request.user,
            seccion__fecha_desde__year=year_selected
        ).distinct()
        filtro = self.request.GET.get('filter')
        if filtro:
            lista_secciones_docente = lista_secciones_docente.filter(
                Q(seccion__codigo__icontains=filtro)|Q(seccion__semestre__nombre__icontains=filtro)
            )
        data = []
        for seccion_docente in lista_secciones_docente:
            data.append({
                'id': seccion_docente.seccion.id,
                'codigo': seccion_docente.seccion.codigo,
                'semestre': seccion_docente.seccion.get_semestre_nombre(),
                'fecha_desde': seccion_docente.seccion.fecha_desde,
                'fecha_hasta': seccion_docente.seccion.fecha_hasta,
            })
        return data

    def get_context_data(self, **kwargs):
        context = super(MantenedorSeccionesDocente, self).get_context_data(**kwargs)
        lista_agnos = (list(DocenteSeccion.objects.all().values_list('seccion__fecha_desde__year',flat=True)) or [])
        agno_siguiente = timezone.now().year+1
        if agno_siguiente not in lista_agnos:
            lista_agnos.append(agno_siguiente)
        context['years'] = lista_agnos
        context['filter'] = self.request.GET.get('filter')
        context['year_selected'] = int(self.request.GET.get('year')) if self.request.GET.get('year') else None
        return context

class ListarParticipantes(ListView):
    template_name = 'docente/seccion/content_participantes.html'
    paginate_by = 10
    model = AlumnoSeccion

    def get_queryset(self):
        lista_alumnos_seccion = AlumnoSeccion.objects.filter(
            seccion_id=self.kwargs['seccion_id'],
            usuario__is_staff=True
        ).distinct()
        data = []
        for alumno_seccion in lista_alumnos_seccion:
            rut = alumno_seccion.usuario.username.split('@')[0]
            data.append({
                'rut': validar_rut.format_rut_without_dots(rut),
                'nombre_completo': alumno_seccion.usuario.get_full_name(),
                'correo': alumno_seccion.usuario.email.upper(),
                'id': alumno_seccion.id,
            })
        return data

class MantenedorActividad(RoyalGuard,ListView):
    template_name = 'docente/actividad/index.html'
    paginate_by = 10
    model = Actividad

    def get_queryset(self):
        lista_actividades = Actividad.objects.filter(seccion_id=self.kwargs['seccion_id']).order_by('orden')
        filtro = self.request.GET.get('filter')
        if filtro:
            lista_actividades = lista_actividades.filter(
                Q(nombre__icontains=filtro)|Q(descripcion__icontains=filtro)|
                Q(seccion__codigo__icontains=filtro)|Q(seccion__semestre__nombre__icontains=filtro)|
                Q(fase__nombre__icontains=filtro)|Q(tipo_entrada__nombre__icontains=filtro)
            )
        return lista_actividades

    def get_context_data(self, **kwargs):
        context = super(MantenedorActividad, self).get_context_data(**kwargs)
        context['seccion'] = self.kwargs['seccion_id']
        context['filter'] = self.request.GET.get('filter')
        return context

class CrearActividad(RoyalGuard,JsonGenericView, CreateView):
    model = Actividad
    form_class = ActividadModelForm
    template_name = 'docente/actividad/content_crear.html'

    def get_initial(self):
        initial = self.request.GET.dict()
        initial['seccion_id'] = self.kwargs['seccion_id']
        return initial

    def get_context_data(self, **kwargs):
        context = super(CrearActividad, self).get_context_data(**kwargs)
        context['seccion'] = self.kwargs['seccion_id']
        return context

class ActualizarActividad(RoyalGuard,JsonGenericView, UpdateView):
    model = Actividad
    form_class = ActividadModelForm
    template_name = 'docente/actividad/content_actualizar.html'

    def get_initial(self):
        return {
            'seccion_id':self.kwargs['seccion_id'],
        }

class EliminarActividad(RoyalGuard,DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Actividad.objects.filter(id=self.kwargs['pk'])
        return queryset
    
    def finalize_response(self, request, response, *args, **kwargs):
        return JsonResponse({
            'estado': '0',
            'respuesta': 'Actividad eliminada con exito!'
        }, status=200,safe=False)

""" fin bloque seccion docente"""