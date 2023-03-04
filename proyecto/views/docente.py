from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.db.models.deletion import ProtectedError
from django.db.models import Q
from django.db.models import Max
from django.views.generic import ListView,TemplateView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from proyecto.auth import RoyalGuard
from function import JsonGenericView
from django.utils import timezone
from function import validar_rut
import base64
# models
from proyecto.models import DocenteSeccion
from proyecto.models import AlumnoSeccion
from proyecto.models import Actividad
from proyecto.models import ActividadRespuestaProyecto,Seccion
from proyecto.models import Proyecto
# forms
from proyecto.content import ActividadModelForm
# serializer
from proyecto.json import ProyectoSerializer

""" inicio bloque seccion docente"""

class MantenedorSeccionesDocente(RoyalGuard,ListView):
    template_name = 'docente/seccion/index.html'
    paginate_by = 10
    model = DocenteSeccion

    def dispatch(self, request, *args, **kwargs):
        tipo_configuracion = request.GET.get('configuration')
        seccion_seleccionada = request.GET.get('selected')
        if tipo_configuracion and seccion_seleccionada:
            resultado = Seccion.objects.get(pk=seccion_seleccionada).set_configuracion_base(tipo_configuracion,request.user)
            if resultado:
                return redirect(f"/docente/seccion/{seccion_seleccionada}/actividades/")
        return super(MantenedorSeccionesDocente, self).dispatch(request, *args, **kwargs)

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
                'con_alumnos': True if len(AlumnoSeccion.objects.filter(seccion=seccion_docente.seccion))>0 else False,
                'con_actividades': True if len(Actividad.objects.filter(seccion=seccion_docente.seccion))>0 else False,
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

class ListarParticipantes(RoyalGuard,ListView):
    template_name = 'docente/participantes/index.html'
    paginate_by = 10
    model = AlumnoSeccion

    def get_queryset(self):
        filter = self.request.GET.get('filter')
        lista_alumnos_seccion = AlumnoSeccion.objects.filter(
            seccion_id=self.kwargs['seccion_id'],
            usuario__is_staff=True
        ).distinct()
        if filter:
            lista_alumnos_seccion = lista_alumnos_seccion.filter(
                Q(usuario__first_name__icontains=filter) | Q(usuario__last_name__icontains=filter) | 
                Q(usuario__username__icontains=filter) | Q(usuario__email__icontains=filter),
            )
        data = []
        for alumno_seccion in lista_alumnos_seccion:
            rut = alumno_seccion.usuario.username.split('@')[0]

            estado = 'No definido por el alumno'
            clase = 'text-gray'
            url =''
            proyecto = Proyecto.objects.filter(alumno_seccion=alumno_seccion).last()
            if proyecto and proyecto.is_pendiente:
                estado = 'Pendiente Aprobación'
                clase = 'text-warning'
                url = f'/docente/proyecto/{proyecto.id}/estado/'
            elif proyecto and proyecto.is_rechazado:
                estado = 'Rechazado'
                clase = 'text-danger'
                url = f'/docente/proyecto/{proyecto.id}/estado/'
            elif proyecto and proyecto.is_aprobado:
                estado = 'Aprobado'
                clase = 'text-success'
                url = f'/docente/proyecto/{proyecto.id}/avances/'

            data.append({
                'rut': validar_rut.format_rut_without_dots(rut),
                'nombre_completo': alumno_seccion.usuario.get_full_name(),
                'correo': alumno_seccion.usuario.email.upper(),
                'id': alumno_seccion.id,
                'proyecto': proyecto,
                'estado':estado,
                'clase':clase,
                'url':url
            })
        return data

    def get_context_data(self, **kwargs):
        context = super(ListarParticipantes, self).get_context_data(**kwargs)
        context['con_actividades'] = True if len(Actividad.objects.filter(seccion_id=self.kwargs['seccion_id']))>0 else False
        context['filter'] = self.request.GET.get('filter')
        return context

class MantenedorActividad(RoyalGuard,TemplateView):
    template_name = 'docente/actividad/index.html'
    # paginate_by = 10
    model = Actividad

    def get_queryset(self):
        lista_actividades = Actividad.objects.filter(seccion_id=self.kwargs['seccion_id']).order_by('orden')
        filtro = self.request.GET.get('filter')
        if filtro:
            lista_actividades = lista_actividades.filter(
                Q(nombre__icontains=filtro)|Q(descripcion__icontains=filtro)|
                Q(seccion__codigo__icontains=filtro)|Q(seccion__semestre__nombre__icontains=filtro)|
                Q(tipo_entrada__nombre__icontains=filtro)
            )
        return lista_actividades

    def get_context_data(self, **kwargs):
        context = super(MantenedorActividad, self).get_context_data(**kwargs)
        context['seccion'] = self.kwargs['seccion_id']
        context['filter'] = self.request.GET.get('filter')
        actividades =[]
        for actividad in self.get_queryset():
            actividades.append({
                'orden_formateado':actividad.orden_formateado,
                'nombre':actividad.nombre,
                'descripcion':actividad.descripcion,
                'depende_de':actividad.depende_de,
                'tipo_entrada':actividad.tipo_entrada,
                'seccion':actividad.seccion,
                'id':actividad.id,
                'ind_base':actividad.ind_base,
            })
        context['object_list'] = sorted(actividades, key=lambda d: d['orden_formateado'])
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
        initial = self.request.GET.dict()
        initial['seccion_id'] = self.kwargs['seccion_id']
        return initial
        
class EliminarActividad(RoyalGuard,DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from django.db.models import F
        queryset = Actividad.objects.filter(
            Q(actividad_padre_id=self.kwargs['pk'])|
            Q(actividad_padre__actividad_padre_id=self.kwargs['pk'])|
            Q(id=self.kwargs['pk'])
        ).order_by(F('actividad_padre_id').desc(nulls_last=True),'id','orden')
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        try:
            for obj in queryset:
                self.perform_destroy(obj)
            return JsonResponse({
                'estado': '0',
                'respuesta': 'Actividad eliminada con exito!'
            }, status=200,safe=False)

        except ProtectedError as e:
            return JsonResponse(status=423, data={'detail':str(e)})
        
class ProyectoActualizar(RoyalGuard,GenericAPIView, UpdateModelMixin):
    serializer_class = ProyectoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return  Proyecto.objects.filter(pk=self.kwargs.get('pk'))

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def finalize_response(self, request, response, *args, **kwargs):
        proyecto = self.get_object()
        return JsonResponse({
            'estado': '0',
            'respuesta': f'Proyecto {"aprobado" if proyecto.is_aprobado else "rechazado"}!'
        }, status=200,safe=False)
""" fin bloque seccion docente"""