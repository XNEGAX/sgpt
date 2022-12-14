from django.shortcuts import redirect
from django.urls import resolve,reverse
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django.db.models.functions import Lower
from django.views.generic import View
from apps.guard.auth import RoyalGuard
from function import ConsultaBD
# models
from ..models.usuarios import UsuarioPerfilActivo
from ..models.usuarios import UsuarioPerfilModulo
from apps.guard.models import Parametro
class Salir(LogoutView):
    def get(self, request, *args, **kwargs):
        rediredct_login = f'/users/login/?next=/'
        return redirect(rediredct_login)


class CambioPerfil(RoyalGuard,View):
    def get(self, request):
        perfil_invitado = Parametro.objects.filter(nombre='perfil_invitado').values('metadatos').last()['metadatos']['perfil_id']
        perfil_activo = UsuarioPerfilActivo.objects.get(usuario=request.user).perfil_id
        perfiles_disponibles = UsuarioPerfilModulo.objects.filter(
            usuario=request.user).values('perfil_id','perfil__nombre'
        ).exclude(
            perfil_id__in=[perfil_invitado,perfil_activo]
        ).annotate(url_logo_perfil=Lower( Concat(Value('/static/udla/img/'),'perfil__nombre',Value('.png'),output_field=CharField())) ).distinct()
        context = {
            'perfil_activo':perfil_activo,
            'perfiles_disponibles':perfiles_disponibles
        }
        return render(request, 'guard/usuarios/content_cambio_perfil.html',context)

    def post(self,request):
        perfil = request.POST.get('perfil')
        UsuarioPerfilActivo.objects.filter(usuario=request.user).update(perfil_id=perfil)
        data = ConsultaBD('public.sp_web_get_permisos_modulo_usuario',(request.user.id,)).execute_proc()
        if len(data)>0:
            request.session['perfil_activo']=data[0].get('perfil_activo')
            request.session['cantidad_perfiles']=data[0].get('cantidad_perfiles')
            request.session['modulos']=data[0].get('modulos')
            submodulo_list = []
            for modulo in data[0].get('modulos'):
                if modulo.get('submodulos'):
                    for submodulo in modulo.get('submodulos'):
                        submodulo_list.append(reverse(submodulo.get('url')))
                request.session['submodulo_list']=submodulo_list
        return redirect('home:home')