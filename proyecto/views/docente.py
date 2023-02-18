from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from proyecto.auth import RoyalGuard
from function import JsonGenericView
# models
from proyecto.models import DocenteSeccion
from proyecto.models import Actividad
# forms
from proyecto.content import ActividadModelForm

""" inicio bloque seccion docente"""

class MantenedorSeccionesDocente(RoyalGuard,ListView):
    template_name = 'docente/seccion/index.html'
    paginate_by = 10
    model = DocenteSeccion

    def get_queryset(self):
        lista_secciones_docente = DocenteSeccion.objects.filter(usuario=self.request.user).distinct()
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

class MantenedorActividad(RoyalGuard,ListView):
    template_name = 'docente/actividad/index.html'
    paginate_by = 10
    model = Actividad

    def get_queryset(self):
        lista_actividades = Actividad.objects.filter(seccion_id=self.kwargs['seccion_id']).order_by('orden')
        filtro = self.request.GET.get('filter')
        if filtro:
            lista_actividades = lista_actividades.filter(
                Q(nombre__icontains=filtro)|Q(nombre__icontains=filtro)|Q(descripcion__icontains=filtro)|
                Q(seccion__codigo__icontains=filtro)|Q(seccion__semestre__nombre__icontains=filtro)|
                Q(seccion__fase__nombre__icontains=filtro)|Q(seccion__descripcion__icontains=filtro)|
                Q(seccion__tipo_entrada__nombre__icontains=filtro)
            )
            print(lista_actividades.query)
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

class ActualizarActividad(JsonGenericView, UpdateView):
    model = Actividad
    form_class = ActividadModelForm
    template_name = 'docente/actividad/content_actualizar.html'

    def get_initial(self):
        print(self.kwargs)
        return {
            'seccion_id':self.kwargs['seccion_id'],
        }

def eliminar_actividad(request,pk):
    Actividad.objects.filter(pk=pk).delete()
    return JsonResponse({
        'estado': '0',
        'respuesta': 'Actividad eliminada con exito!'
    }, status=200,safe=False)

""" fin bloque seccion docente"""