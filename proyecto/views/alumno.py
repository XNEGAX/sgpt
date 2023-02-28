from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import ListView,TemplateView,View
from django.views.generic import CreateView
from django.views.generic import UpdateView
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from proyecto.auth import RoyalGuard
from function import JsonGenericView
from django.utils import timezone
# models
from proyecto.models import AlumnoSeccion
from proyecto.models import Actividad
from proyecto.models import Proyecto
# forms
from proyecto.content import ProyectoModelForm

class ListarSeccionesAlumno(RoyalGuard,ListView):
    template_name = 'alumno/seccion/index.html'
    paginate_by = 10
    model = AlumnoSeccion

    def get_queryset(self):
        lista_alumnos_seccion = AlumnoSeccion.objects.filter(
            usuario=self.request.user,
        ).distinct().order_by('-id')
        data = []
        for alumno_seccion in lista_alumnos_seccion:
            docente_seccion = alumno_seccion.seccion.fk_seccion_docente_seccion.all().last()
            profesor = docente_seccion.usuario.get_full_name() if docente_seccion else 'Por asignar'
        
            estado = 'Proyecto por definir'
            motivo_rechazo = ''
            accion = 1
            url = f"/alumno/seccion/{alumno_seccion.id}/proyecto/crear/"
            proyecto = Proyecto.objects.filter(alumno_seccion=alumno_seccion).last()
            if proyecto and proyecto.is_pendiente:
                estado = 'Proyecto pendiente Aprobación'
                url = f"/alumno/seccion/proyecto/{proyecto.id}/actualizar/"
                accion = 2
            elif proyecto and proyecto.is_rechazado:
                estado = 'Proyecto rechazado'
                motivo_rechazo = proyecto.motivo_rechazo
                url = f"/alumno/seccion/proyecto/{proyecto.id}/actualizar/"
                accion = 3
            elif proyecto and proyecto.is_aprobado:
                estado = 'Proyecto aprobado'
                url = f"/alumno/seccion/proyecto/{proyecto.id}/actividades/"
                accion = 0
                
            data.append({
                'id': alumno_seccion.id,
                'seccion': alumno_seccion.seccion,
                'profesor': profesor,
                'fecha_desde':alumno_seccion.seccion.fecha_desde,
                'fecha_hasta':alumno_seccion.seccion.fecha_hasta,
                'estado':estado.upper(),
                'con_preguntas':len(docente_seccion.seccion.fk_seccion_actividad.all())>0,
                'url':url,
                'accion':accion,
                'motivo_rechazo':motivo_rechazo.upper()
            })
        return data
    

class CrearProyectoTitulo(JsonGenericView,CreateView):
    model = Proyecto
    form_class = ProyectoModelForm
    template_name = 'alumno/proyecto/content_crear.html'

    def get_initial(self):
        initial = self.request.GET.dict()
        initial['alumno_seccion_id'] = self.kwargs['alumno_seccion_id']
        return initial

    def get_context_data(self, **kwargs):
        context = super(CrearProyectoTitulo, self).get_context_data(**kwargs)
        context['alumno_seccion_id'] = self.kwargs['alumno_seccion_id']
        return context
    
class ActualizarProyectoTitulo(JsonGenericView, UpdateView):
    model = Proyecto
    form_class = ProyectoModelForm
    template_name = 'alumno/proyecto/content_actualizar.html'

class ResponderActvidades(ListView):
    template_name = 'alumno/actividades/index.html'

    def setup(self,request,*args,**kwargs):
        if not Proyecto.objects.filter(alumno_seccion_id=kwargs.get('alumno_seccion_id'),ind_aprobado=True).exists():
            return redirect("proyecto:alumno_seccion_proyecto", alumno_seccion_id=kwargs.get('alumno_seccion_id'))
        return super(ResponderActvidades, self).get_context_data(**kwargs)