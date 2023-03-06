from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import View
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from proyecto.auth import RoyalGuard
from function import JsonGenericView
from django.http import JsonResponse
from django.shortcuts import render
# models
from proyecto.models import AlumnoSeccion
from proyecto.models import Proyecto
from proyecto.models import Gantt
from proyecto.models import ActividadRespuestaProyecto,Actividad
# forms
from proyecto.content import ProyectoModelForm
from proyecto.content import GanttModelForm
# serializer
from proyecto.json import GanttSerializer

class ListarSeccionesAlumno(RoyalGuard,ListView):
    template_name = 'alumno/seccion/index.html'
    paginate_by = 10
    model = AlumnoSeccion

    def get_queryset(self):
        lista_alumnos_seccion = AlumnoSeccion.objects.filter(
            usuario=self.request.user,
        ).distinct()
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
                'motivo_rechazo':motivo_rechazo.upper(),
            })
        return data
    

class CrearProyectoTitulo(RoyalGuard,JsonGenericView,CreateView):
    model = Proyecto
    form_class = ProyectoModelForm
    template_name = 'alumno/seccion/content_crear.html'

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
    template_name = 'alumno/seccion/content_actualizar.html'

class ResponderActvidades(View):
    def get(self,request,proyecto_id):
        proyectos = Proyecto.objects.filter(pk=proyecto_id)
        if not proyectos.filter(in_activo=True).exists():
            proyectos.update(in_activo=False)
            proyectos.filter(pk=proyecto_id).update(in_activo=True)
        # fin cambio de activo
        proyecto = Proyecto.objects.get(pk=proyecto_id)
        if proyecto:
            request.session['proyecto'] = {
                'url':proyecto.url,
                'actividades_menu':proyecto.actividades_menu
            }
        breackcrum = f'<h5 class="fw-bold py-3 mb-4"><span class="text-muted fw-light">Proyecto / </span>{proyecto.nombre.capitalize()}</h5>'
        actividades= proyecto.actividades_seccion.filter(actividad_padre=self.request.GET.get('actividad')).order_by('orden')
        if len(actividades)==0:
            actividades = proyecto.actividades_seccion.filter(id=self.request.GET.get('actividad')).order_by('orden')
            if len(actividades)==1:
                if actividades[0].actividad_padre:
                    breackcrum = f'''<h5 class="fw-bold py-3 mb-4"><span class="text-muted fw-light">{proyecto.nombre.capitalize()} / {actividades[0].actividad_padre.nombre.capitalize()} / </span>{actividades[0].nombre.capitalize()}</h5>'''
                else:
                    breackcrum = f'''<h5 class="fw-bold py-3 mb-4"><span class="text-muted fw-light">{proyecto.nombre.capitalize()} / </span>{actividades[0].nombre.capitalize()}</h5>'''
        else:
            if self.request.GET.get('actividad'):
                breackcrum = f'<h5 class="fw-bold py-3 mb-4"><span class="text-muted fw-light">{proyecto.nombre.capitalize()} / </span>{actividades[0].actividad_padre.nombre.capitalize()}</h5>'

        context = {
            'actividades_seccion':actividades,
            'breackcrum':breackcrum,
            'actividad_enviada':self.request.GET.get('actividad'),
            'object_list':proyecto
        }
        return render(request, 'alumno/proyecto/index.html',context=context)

    def post(self,request,proyecto_id):
        #preparamos la data
        data = request.POST.get('actividad_valor')
        actividad = Actividad.objects.get(pk=request.POST.get('actividad_id'))
        publicar = request.POST.get('publicar')
        kwargs = {}

        respuesta = ActividadRespuestaProyecto.objects.filter(
            proyecto_id=proyecto_id,
            actividad=actividad
        )


        if actividad.tipo_entrada.ind_archivo and actividad.tipo_entrada.ind_multiple:
            if respuesta.exists():
                data = respuesta.last().respuesta
            kwargs['nombre'] = request.POST.get('nombre_archivo_actividad')
            kwargs['archivo'] = request.FILES.get('actividad_valor')
            kwargs['indice'] = request.POST.get('indice')
            
        if respuesta.exists():
            obj = respuesta.last()
            obj.respuesta = data
            obj.ind_publicada = True if publicar else False
            obj.save(**kwargs)
            mensaje = 'Actividad actualizada!'
        else:
            obj = ActividadRespuestaProyecto(
                proyecto_id = proyecto_id,
                actividad = actividad,
                respuesta = data,
                responsable = request.user,
                ind_publicada = True if publicar else False
            )
            obj.save(**kwargs)
            mensaje = 'Actividad creado!'
        estado = '3'
        if publicar:
            estado = '0'
        return JsonResponse({
            'estado': estado,
            'mensaje': mensaje
        }, status=200,safe=False)

class CrearTareaProyecto(JsonGenericView,CreateView):
    model = Gantt
    form_class = GanttModelForm
    template_name = 'alumno/proyecto/content_crear.html'

    def get_initial(self):
        initial = self.request.GET.dict()
        initial['proyecto_id'] = self.kwargs['proyecto_id']
        return initial

    def get_context_data(self, **kwargs):
        context = super(CrearTareaProyecto, self).get_context_data(**kwargs)
        context['proyecto_id'] = self.kwargs['proyecto_id']
        return context
    
class ActualizaTareaProyecto(JsonGenericView, UpdateView):
    model = Gantt
    form_class = GanttModelForm
    template_name = 'alumno/proyecto/content_actualizar.html'

class EliminarTareaProyecto(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GanttSerializer
    queryset = Gantt.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse({
            'estado': '0',
            'respuesta': 'Tarea eliminada!'
        }, status=200,safe=False)


         