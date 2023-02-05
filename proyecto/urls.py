from django.urls import path
from proyecto.views import Home
from proyecto.views import Salir
from proyecto.views import CambioPerfil
from proyecto.views import Error403

from proyecto.views import ImpersonarUsuario
from proyecto.views.mantenedor import MantenedorUsuario
from proyecto.views.mantenedor import CrearUsuario
from proyecto.views.mantenedor import ActualizarUsuario

from proyecto.views.mantenedor import MantenedorSeccion
from proyecto.views.mantenedor import CrearSeccion
from proyecto.views.mantenedor import ActualizarSeccion
from proyecto.views.mantenedor import eliminar_seccion

from proyecto.views.mantenedor import mantenedor_fases
from proyecto.views.mantenedor import mantenedor_proyecto
from proyecto.views.mantenedor import lista_secciones
from proyecto.views.mantenedor import lista_alumnos
from proyecto.views.mantenedor import mantenedor_actividades
from proyecto.views.mantenedor import mantenedor_configuracionBase



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

    path('mantenedor/secciones/', MantenedorSeccion.as_view(), name="mantenedor_secciones"),
    path('mantenedor/seccion/crear/', CrearSeccion.as_view(), name="mantenedor_seccion_crear"),
    path('mantenedor/seccion/<pk>/actualizar/', ActualizarSeccion.as_view(), name="mantenedor_seccion_actualizar"),
    path('mantenedor/seccion/<pk>/eliminar/', eliminar_seccion, name="mantenedor_seccion_eliminar"),
    
    path('mantenedor/fases/', mantenedor_fases, name="mantenedor_fases"),
    path('mantenedor/proyecto/', mantenedor_proyecto, name="mantenedor_proyecto"),
    path('lista/secciones/', lista_secciones, name="lista_secciones"),
    path('lista/alumnos/', lista_alumnos, name="lista_alumnos"),

    path('mantenedor/actividad/', mantenedor_actividades, name="mantenedor_actividades"),
    path('mantenedor/configuracionBase/', mantenedor_configuracionBase, name="mantenedor_configuracionBase"),
]