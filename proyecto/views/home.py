from django.shortcuts import render
from django.views.generic import View
from proyecto.auth import RoyalGuard
from function import validar_rut
import base64
from function import getDatetime
from io import BytesIO
import numpy as np 
import matplotlib.pyplot as plt
from django.db.models import Count
from django.forms.models import model_to_dict
# models
from proyecto.models.log import Log
from proyecto.models import PerfilUsuario
from proyecto.models import Proyecto
from proyecto.models import ActividadRespuestaProyecto

def getGraphLog(ano=getDatetime().year):
    meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    logs = Log.objects.filter(fecha__year=ano).values('accion','fecha__month').annotate(total=Count('accion')).order_by('fecha__month')
    creados = [0,0,0,0,0,0,0,0,0,0,0,0]
    modificados = [0,0,0,0,0,0,0,0,0,0,0,0]
    eliminados = [0,0,0,0,0,0,0,0,0,0,0,0]
    for indice in range(len(meses)):
        for log in logs:
            if  indice == log.get('fecha__month'):
                if log.get('accion') == 1:
                    creados[indice] = log.get('total')
                if log.get('accion') == 2:
                    modificados[indice] = log.get('total')
                if log.get('accion') == 3:
                    eliminados[indice] = log.get('total')
    
    X_axis = np.arange(len(meses))
    
    plt.bar(X_axis + 0.3, creados, 0.3, label = 'Creados', align='center')
    plt.bar(X_axis + 0.6, modificados, 0.3, label = 'Modificados', align='center')
    plt.bar(X_axis + 0.9, eliminados, 0.3, label = 'Eliminados', align='center')
    
    plt.xticks(X_axis, meses, rotation='vertical')
    plt.xlabel("Meses")
    plt.ylabel("Actividades completas x mes")
    plt.ylabel("Registros x acción")
    plt.title("Registros x mes")
    plt.legend()
    plt.show()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode('utf-8')
    plt.close()
    buffer.close()
    return graph

def getGraphActividadesxMes(proyecto):
    meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    actividades = []
    for indice in range(len(meses)):
        cantidad = ActividadRespuestaProyecto.objects.filter(proyecto=proyecto,fecha__month=indice+1,actividad__ind_base=False).count()
        actividades.append(cantidad)
        
    
    X_axis = np.arange(len(meses))
    
    plt.bar(X_axis + 0.3, actividades, 0.3, label = 'Actividades', align='center')
    plt.xticks(X_axis, meses, rotation='vertical')
    plt.xlabel("2023")
    plt.setp(plt.ylabel("Cantidad x mes"), color='#EB6923')
    plt.setp(plt.title("Avance del proyecto x mes"), color='#EB6923')
    plt.subplots_adjust(bottom=0.25)
    plt.legend()
    plt.show()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode('utf-8')
    plt.close()
    buffer.close()
    return graph

class Home(RoyalGuard,View):
    def get(self, request):
        context = {}
        if 'proyecto' in request.session:
            del request.session['proyecto']
        if request.session.get('perfil_activo').upper() =='ADMINISTRADOR':
            #log last 
            log_data = []
            logs = Log.objects.all().order_by('-fecha')[:5]
            for log in logs:
                log_data.append({
                    'modelo_nombre':log.modelo.name,
                    'accion_nombre':log.accion_nombre,
                    'fecha':log.fecha,
                    'responsable':log.responsable.get_full_name(),
                    'instance':log.instancia_recuperada
                })
            context['transacciones'] = log_data
            context['graph_log'] = getGraphLog()

        elif request.session.get('perfil_activo').upper() =='PROFESOR':
            secciones_docente = self.request.user.fk_usuario_docente_seccion.all()
            lista_agnos = (list(secciones_docente.values_list('seccion__fecha_desde__year',flat=True)) or [])
            year_selected = self.request.GET.get('year',getDatetime().year)
            context['secciones_docente'] = secciones_docente.filter(seccion__fecha_desde__year=year_selected)
            context['years'] = lista_agnos
            context['year_selected'] = year_selected

            data = []
            for seccion_docente in secciones_docente.filter(seccion__fecha_desde__year=year_selected):
                temp_seccion = model_to_dict(seccion_docente.seccion)
                temp_seccion['alumnos'] = []
                for alumno_seccion in seccion_docente.seccion.fk_seccion_alumno_seccion.all():
                    rut = alumno_seccion.usuario.username.split('@')[0]
                    temp_proy = Proyecto.objects.filter(alumno_seccion=alumno_seccion).last()
                    temp_seccion['alumnos'].append({
                        'rut': validar_rut.format_rut_without_dots(rut),
                        'nombre_completo': alumno_seccion.usuario.get_full_name(),
                        'id': temp_proy.id if temp_proy else None,
                    })
                data.append(temp_seccion)
            context['lista_secciones_docente'] = data
        else:
            context['porcentaje_avance'] = 0
            context['avance_x_captulo'] = []
            proyecto = Proyecto.objects.filter(in_activo=True,ind_aprobado=True,alumno_seccion__usuario=request.user).last()
            if proyecto:
                request.session['proyecto'] = {
                    'url':proyecto.url,
                    'actividades_menu':proyecto.actividades_menu
                }
                context['graph_actividadesxmes'] = getGraphActividadesxMes(proyecto)
                context['porcentaje_avance'] =proyecto.porcentaje_avance
                context['avance_x_captulo'] =proyecto.avance_x_captulo

        return render(request, 'home/index.html', context)