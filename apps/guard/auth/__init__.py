from django.urls import resolve
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from function import ConsultaBD
from apps.guard.models import UsuarioPerfilRol
from microsoft_auth.backends import MicrosoftAuthenticationBackend
from microsoft_auth.client import MicrosoftClient
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class CustomAuthBackendMicrosoft(MicrosoftAuthenticationBackend):
    def authenticate(self, request, code=None):
        self.microsoft = MicrosoftClient(request=request)
        user = None
        if code is not None:
            token = self.microsoft.fetch_token(code=code)
            if "access_token" in token and self.microsoft.valid_scopes(token["scope"]):
                user = self._authenticate_user()
        if user is not None:
            self._call_hook(user)
            modulos = ConsultaBD('public.sp_web_get_permisos_modulo_usuario',(user.id,)).execute()
            if len(modulos)>0:
                request.session['perfil']=modulos[0].get('perfil')
                request.session['modulos']=modulos[0].get('modulos')
        return user

class CustomAuthBackendDjango(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                modulos = ConsultaBD('public.sp_web_get_permisos_modulo_usuario',(user.id,)).execute()
                if len(modulos)>0:
                    request.session['perfil']=modulos[0].get('perfil')
                    request.session['modulos']=modulos[0].get('modulos')
                return user



class RoyalGuard(LoginRequiredMixin):
    login_url = '/admin/login/'

    def dispatch(self, request, *args, **kwargs):
        rediredct_login = f'/admin/login/?next={request.path}'
        if request.user and request.user.is_authenticated:
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