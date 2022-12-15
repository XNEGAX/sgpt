from django.urls import path
from apps.guard.views.usuarios import Salir
from apps.guard.views.usuarios import CambioPerfil
from apps.guard.views.errores import Error403
from apps.guard.views.mantenedores import MantenedorUsuario
from apps.guard.views.mantenedores import CrearUsuario
from apps.guard.views.mantenedores import ActualizarUsuario

app_name = 'guard'

urlpatterns = [
    path('403/', Error403.as_view(), name="403"),
    path("salir", Salir.as_view(), name="salir"),
    path("perfil/cambio/", CambioPerfil.as_view(), name="cambio_perfil"),
    path("mantenedor/usuario/", MantenedorUsuario.as_view(), name="mantenedor_usuario"),
    path("mantenedor/usuario/crear/", CrearUsuario.as_view(), name="mantenedor_usuario_crear"),
    path('mantenedor/usuario/actualizar/', ActualizarUsuario.as_view(), name="mantenedor_usuario_actualizar")
]