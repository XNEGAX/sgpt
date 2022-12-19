from django.urls import path
from proyecto.views import Home
from proyecto.views import Salir
from proyecto.views import CambioPerfil
from proyecto.views import Error403
from proyecto.views import ImpersonarUsuario
from proyecto.views.mantenedor import MantenedorUsuario
from proyecto.views.mantenedor import CrearUsuario
from proyecto.views.mantenedor import ActualizarUsuario
from proyecto.views.mantenedor import mantenedor_actividades

app_name = 'proyecto'

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('403/', Error403.as_view(), name="403"),
    path("salir", Salir.as_view(), name="salir"),
    path("perfil/cambio/", CambioPerfil.as_view(), name="cambio_perfil"),
    path("usuario/impersonar/", ImpersonarUsuario.as_view(), name="impersonar_usuario"),
    path("mantenedor/usuario/", MantenedorUsuario.as_view(), name="mantenedor_usuario"),
    path("mantenedor/usuario/crear/", CrearUsuario.as_view(), name="mantenedor_usuario_crear"),
    path('mantenedor/usuario/<pk>/actualizar/', ActualizarUsuario.as_view(), name="mantenedor_usuario_actualizar"),
    path('mantenedor/usuario/actualizar/', ActualizarUsuario.as_view(), name="mantenedor_usuario_actualizar"),
    path('mantenedor/actividad/', mantenedor_actividades, name="mantenedor_actividades")
]