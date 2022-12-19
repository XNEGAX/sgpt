from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.shortcuts import render
from proyecto.auth import RoyalGuard
from proyecto.auth import set_aditional_paramas
from django.views.generic import View
from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django.db.models.functions import Lower
from django.contrib.auth import login
# models
from proyecto.models import Parametro
from proyecto.models import PerfilUsuarioActivo
from proyecto.models import PerfilUsuario
from django.contrib.auth.models import User

class Salir(LogoutView):
    def get(self, request, *args, **kwargs):
        rediredct_login = f'/users/login/?next=/'
        return redirect(rediredct_login)

class CambioPerfil(RoyalGuard,View):
    def get(self, request):
        perfil_invitado = Parametro.objects.filter(nombre='perfil_invitado').values('metadatos').last()['metadatos']['perfil_id']
        perfil_activo = PerfilUsuarioActivo.objects.get(usuario=request.user).perfil_id
        perfiles_disponibles = PerfilUsuario.objects.filter(usuario=request.user).values(
            'perfil_id','perfil__nombre'
        ).exclude(
            perfil_id__in=[perfil_invitado,perfil_activo]
        ).annotate(url_logo_perfil=Lower( Concat(Value('/static/udla/img/'),'perfil__nombre',Value('.png'),output_field=CharField())) ).distinct()
        context = {
            'perfil_activo':perfil_activo,
            'perfiles_disponibles':perfiles_disponibles
        }
        return render(request, 'control/content_cambio_perfil.html',context)

    def post(self,request):
        perfil = request.POST.get('perfil')
        PerfilUsuarioActivo.objects.filter(usuario=request.user).update(perfil_id=perfil)
        set_aditional_paramas(request.user,request)
        return redirect('proyecto:home')


class Error403(View):
    def get(self, request):
        return render(request, 'control/errores.html',context={'estado':403},status=403)


class ImpersonarUsuario(RoyalGuard,View):
    def post(self, request):
        impersonate = User.objects.get(id=request.POST.get('usuario_id'))
        login(request, impersonate)
        set_aditional_paramas(impersonate,request)
        return redirect('proyecto:home')