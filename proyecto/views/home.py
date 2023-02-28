from django.shortcuts import render
from django.views.generic import View
from proyecto.auth import RoyalGuard
from function import validar_rut
# models
from proyecto.models.log import Log
from proyecto.models import PerfilUsuario


class Home(RoyalGuard,View):
    def get(self, request):
        context = {}
        if request.session.get('perfil_activo').upper() =='ADMINISTRADOR':
            log_data = []
            logs = Log.objects.all().order_by('-fecha')[:10]
            for log in logs:
                log_data.append({
                    'modelo_name':log.modelo.name.title(),
                    'accion_nombre':log.accion_nombre,
                    'fecha':log.fecha,
                    'responsable':log.responsable.get_full_name(),
                    'instance':log.instancia_recuperada
                })
            context['transacciones'] = log_data
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
        return render(request, 'home/index.html', context)