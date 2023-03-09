from django.shortcuts import render
from django.views.generic import View
from proyecto.auth import RoyalGuard
from function import validar_rut
# models
from proyecto.models.log import Log
from proyecto.models import PerfilUsuario
from proyecto.models import Proyecto
import base64
from function import getDatetime
import numpy as np 
import matplotlib.pyplot as plt
from django.db.models import Count

def getGraphLog(ano=getDatetime().year):
    from io import BytesIO
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
    plt.xlabel("Groups")
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
            lista_perfil_usuarios = PerfilUsuario.objects.filter(
                perfil__nombre='ALUMNO',usuario__is_staff=True
            ).exclude(usuario__is_superuser=True)
            data = []
            for perfil_usuario in lista_perfil_usuarios:
                if perfil_usuario.is_perfil_habilitado:
                    rut = perfil_usuario.usuario.username.split('@')[0]
                    data.append({
                        'rut': validar_rut.format_rut_without_dots(rut),
                        'nombre_completo': perfil_usuario.usuario.get_full_name(),
                        'id': perfil_usuario.usuario.id,
                    })
            context['lista_alumnos'] = sorted(data, key=lambda d: d['nombre_completo'])
        else:
            proyecto = Proyecto.objects.filter(in_activo=True,ind_aprobado=True,alumno_seccion__usuario=request.user).last()
            if proyecto:
                print(proyecto.descripcion.encode('latin_1'))
                request.session['proyecto'] = {
                    'url':proyecto.url,
                    'actividades_menu':proyecto.actividades_menu
                }
        return render(request, 'home/index.html', context)