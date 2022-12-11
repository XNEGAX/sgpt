from django.urls import resolve
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from function import ConsultaBD
from apps.guard.models import UsuarioPerfilRol
from apps.guard.models import Parametro
from apps.guard.models import UsuarioPerfilActivo
from microsoft_auth.backends import MicrosoftAuthenticationBackend
from microsoft_auth.client import MicrosoftClient
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class CustomAuthBackendMicrosoft(MicrosoftAuthenticationBackend):

    def enable_user(self,user):
        if 'edu.udla.cl' in user.email:
            if not user.is_staff:
                """se habilita el usuario"""
                user.is_staff = True
                user.save()
                """se obtienen parametros default"""
                perfil_rol_generico_invitado = Parametro.objects.filter(nombre='perfil_rol_generico_invitado').values('metadatos').last()
                auth_user_auto = Parametro.objects.filter(nombre='auth_user_auto').values('metadatos').last()
                perfil_invitado = Parametro.objects.filter(nombre='perfil_invitado').values('metadatos').last()
                if bool(perfil_rol_generico_invitado) and bool(auth_user_auto) and bool(perfil_invitado):
                    perfil_rol_generico_invitado = int(perfil_rol_generico_invitado['metadatos']['perfil_rol_id'])
                    auth_user_auto = int(auth_user_auto['metadatos']['auth_user_id'])
                    perfil_invitado = int(perfil_invitado['metadatos']['perfil_id'])
                    """se asigna el rol generico - invitado"""
                    UsuarioPerfilRol.objects.update_or_create(
                        perfil_rol_id = perfil_rol_generico_invitado,
                        usuario = user,
                        permiso = '["GET"]',
                        responsable_id = auth_user_auto
                    )
                    """Se asigna perfil activo default"""
                    UsuarioPerfilActivo.objects.update_or_create(
                        perfil_id = perfil_invitado,
                        usuario = user,
                        responsable_id = auth_user_auto
                    )
        else:
            user.delete()
            return redirect('guard:403')

    def authenticate(self, request, code=None):
        self.microsoft = MicrosoftClient(request=request)
        user = None
        if code is not None:
            token = self.microsoft.fetch_token(code=code)
            if "access_token" in token and self.microsoft.valid_scopes(token["scope"]):
                user = self._authenticate_user()
        if user is not None:
            self._call_hook(user)
            self.enable_user(user)
            data = ConsultaBD('public.sp_web_get_permisos_modulo_usuario',(user.id,)).execute_proc()
            if len(data)>0:
                print(data)
                request.session['perfil_activo']=data[0].get('perfil_activo')
                request.session['cantidad_perfiles']=data[0].get('cantidad_perfiles')
                request.session['modulos']=data[0].get('modulos')
                submodulo_list = []
                for modulo in data[0].get('modulos'):
                    if modulo.get('submodulos'):
                        for submodulo in modulo.get('submodulos'):
                            submodulo_list.append(reverse(submodulo.get('url')))
                    request.session['submodulo_list']=submodulo_list
        return user

class RoyalGuard(LoginRequiredMixin):
    login_url = '/admin/login/'

    def dispatch(self, request, *args, **kwargs):
        rediredct_login = f'/admin/login/?next={request.path}'
        if request.user and request.user.is_authenticated and request.path != '/admin':
            url_permitida = UsuarioPerfilRol.objects.filter(
                perfil_rol__perfil__usuarioperfilactivo_set__usuario_id=request.user.id,
                perfil_rol__rol__modulorol_set__modulo__url=resolve(request.path).app_name+':'+resolve(request.path).url_name,
                usuario_id=request.user.id,
                permiso__icontains=request.method
            ).exists()
            if not url_permitida:
                return redirect('guard:403')
        else:
            return redirect(rediredct_login)
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)