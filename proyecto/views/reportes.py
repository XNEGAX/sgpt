from django.views.generic import View
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from function import validar_rut
from proyecto.auth import RoyalGuard
# models
from proyecto.models import *
# forms
from proyecto.content.reporte_configurable_model_form import ReporteConfigurableModelForm
# functions
from function import FuncListDicttoExcel

class ListarReporteConfigurable(RoyalGuard,ListView):
    template_name = 'reportes/index.html'
    paginate_by = 10
    model = ReporteConfigurable

class CrearReporteConfigurable(RoyalGuard,CreateView):
    model = ReporteConfigurable
    form_class = ReporteConfigurableModelForm
    template_name = 'reportes/content_crear.html'
    success_url = reverse_lazy('proyecto:listar_reportes')

    def form_valid(self, form):
        form.instance.responsable = self.request.user
        return super().form_valid(form)

class ActualizaReporteConfigurable(RoyalGuard,UpdateView):
    model = ReporteConfigurable
    form_class = ReporteConfigurableModelForm
    template_name = 'reportes/content_actualizar.html'
    success_url = reverse_lazy('proyecto:listar_reportes')

    def post(self, request, *args, **kwargs):
        if not request.POST._mutable:
            request.POST._mutable = True
        request.POST['responsable'] = request.user
        return super(ActualizaReporteConfigurable, self).post(request, *args, **kwargs)

class EliminarReporteConfigurable(RoyalGuard,DeleteView):
    model = ReporteConfigurable
    template_name = 'reportes/content_eliminar.html'
    success_url = reverse_lazy('proyecto:listar_reportes')


class ExportarReporte(RoyalGuard,View):
    def get(self,request,pk):
        reporte = ReporteConfigurable.objects.get(pk=pk)
        formula = reporte.codigo_fuente
        loc = {}
        parametros = globals()
        parametros['yo'] = request.user
        exec(formula, globals(), loc)
        respuesta = loc['respuesta']
        return FuncListDicttoExcel(reporte.nombre,respuesta).get_excel()
