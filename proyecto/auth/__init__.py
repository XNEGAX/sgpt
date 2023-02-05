import json
from django.urls import resolve
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from function import ConsultaBD
from microsoft_auth.backends import MicrosoftAuthenticationBackend
from microsoft_auth.client import MicrosoftClient
# models
from proyecto.models import Parametro
from proyecto.models import PerfilUsuario
from proyecto.models import PerfilUsuarioActivo

from django.contrib.auth import get_user_model

UserModel = get_user_model()

def set_aditional_paramas(user,request):
    data = ConsultaBD('public.sp_web_get_permisos_modulo_usuario',(user.id,)).execute_proc()
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

class CustomAuthBackendMicrosoft(MicrosoftAuthenticationBackend):

    def enable_user(self,user,request):
        auth_user_auto = Parametro.objects.filter(nombre='auth_user_auto').values('metadatos').last()
        perfil_invitado = Parametro.objects.filter(nombre='perfil_invitado').values('metadatos').last()
        if 'edu.udla.cl' in user.email:
            request.session['not_domain']=False
            if not user.is_staff and bool(auth_user_auto) and perfil_invitado:
                """se habilita el usuario"""
                user.is_staff = True
                user.save()
                """se asignan parametros default"""
                auth_user_auto = int(auth_user_auto['metadatos']['auth_user_id'])
                perfil_invitado = int(perfil_invitado['metadatos']['perfil_id'])
                if not PerfilUsuario.objects.filter(usuario = user).exists():
                    PerfilUsuario.objects.create(
                        perfil_id = perfil_invitado, 
                        usuario = user,
                        responsable_id = auth_user_auto
                    )
                if not PerfilUsuarioActivo.objects.filter(usuario=user).exists():
                    PerfilUsuarioActivo.objects.create(
                        perfil_id = perfil_invitado,
                        usuario = user,
                        responsable_id = auth_user_auto
                    )
        else:
            user.is_active = False
            user.save()
            request.session['not_domain']=True

    def authenticate(self, request, code=None):
        self.microsoft = MicrosoftClient(request=request)
        user = None
        if code is not None:
            token = self.microsoft.fetch_token(code=code)
            if "access_token" in token and self.microsoft.valid_scopes(token["scope"]):
                user = self._authenticate_user()
        if user is not None:
            self._call_hook(user)
            self.enable_user(user,request)
            set_aditional_paramas(user,request)
        return user

class RoyalGuard(LoginRequiredMixin):
    login_url = '/users/login/'

    def dispatch(self, request, *args, **kwargs):
        rediredct_login = f'/users/login/?next={request.path}'
        if request.user and request.user.is_authenticated:
            url_permitida = PerfilUsuario.objects.filter(
                perfil__usuario_perfil_activo_perfil__usuario_id=request.user.id,
                perfil__perfil_modulo_perfil__modulo__url=resolve(request.path).app_name+':'+resolve(request.path).url_name,
                usuario_id=request.user.id,
            ).exists()
            if not url_permitida:
                if request.is_ajax():
                    return HttpResponseForbidden(request)
                return redirect('proyecto:403')
            else:
                request.session['breadcrumb'] =''
                ruta = str(request.path).split('/')
                while("" in ruta):
                    ruta.remove("")
                if len(ruta)==2:
                    request.session['breadcrumb'] = f'<h5 class="fw-bold py-3 mb-4"><span class="text-muted fw-light">{ruta[0].capitalize()} / </span>{ruta[1].capitalize()}</h5>'
                elif len(ruta)==3:
                    request.session['breadcrumb'] = f'<h5 class="fw-bold py-3 mb-4"><span class="text-muted fw-light">{ruta[0].capitalize()} / {ruta[1].capitalize()} / </span>{ruta[2].capitalize()}</h5>'
                elif len(ruta)==1:
                    if ruta[0] != '/':
                        request.session['breadcrumb'] = f'<h5 class="fw-bold py-3 mb-4">{ruta[0].capitalize()}</h5>'
        else:
            return redirect(rediredct_login)
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
