from django.urls import path
from proyecto.views import Home
from proyecto.views import Salir
from proyecto.views import CambioPerfil
from proyecto.views import Error403

from proyecto.views import ImpersonarUsuario
from proyecto.views.mantenedor import MantenedorUsuario
from proyecto.views.mantenedor import CrearUsuario
from proyecto.views.mantenedor import ActualizarUsuario
from proyecto.views.mantenedor import BuscadorUsuario

from proyecto.views.mantenedor import MantenedorSeccion
from proyecto.views.mantenedor import CrearSeccion
from proyecto.views.mantenedor import ActualizarSeccion
from proyecto.views.mantenedor import eliminar_seccion
from proyecto.views.mantenedor import AdministrarSeccion

from proyecto.views.mantenedor import MantenedorFase
from proyecto.views.mantenedor import CrearFase
from proyecto.views.mantenedor import ActualizarFase
from proyecto.views.mantenedor import eliminar_fase

from proyecto.views.docente import MantenedorSeccionesDocente
from proyecto.views.docente import MantenedorActividad
from proyecto.views.docente import CrearActividad
from proyecto.views.docente import ActualizarActividad
from proyecto.views.docente import eliminar_actividad

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
    path('mantenedor/usuario/buscar/', BuscadorUsuario.as_view(), name="mantenedor_usuario_buscar"),

    path('mantenedor/secciones/', MantenedorSeccion.as_view(), name="mantenedor_secciones"),
    path('mantenedor/seccion/crear/', CrearSeccion.as_view(), name="mantenedor_seccion_crear"),
    path('mantenedor/seccion/<pk>/actualizar/', ActualizarSeccion.as_view(), name="mantenedor_seccion_actualizar"),
    path('mantenedor/seccion/<pk>/eliminar/', eliminar_seccion, name="mantenedor_seccion_eliminar"),
    path('mantenedor/seccion/<pk>/administrar/', AdministrarSeccion.as_view(), name="mantenedor_seccion_administar"),
    path('mantenedor/seccion/<pk>/<metodo>/<perfil>/', AdministrarSeccion.as_view(), name="mantenedor_seccion_administar"),
    path('mantenedor/seccion/<pk>/<metodo>/<perfil>/<usuario>/', AdministrarSeccion.as_view(), name="mantenedor_seccion_administar"),

    path('mantenedor/fases/', MantenedorFase.as_view(), name="mantenedor_fases"),
    path('mantenedor/fase/crear/', CrearFase.as_view(), name="mantenedor_fase_crear"),
    path('mantenedor/fase/<pk>/actualizar/', ActualizarFase.as_view(), name="mantenedor_fase_actualizar"),
    path('mantenedor/fase/<pk>/eliminar/', eliminar_fase, name="mantenedor_fase_eliminar"),

    path('docente/secciones/', MantenedorSeccionesDocente.as_view(), name="docente_secciones"),
    path('docente/seccion/<seccion_id>/actividades/', MantenedorActividad.as_view(), name="docente_seccion_actividades"),
    path('docente/seccion/<seccion_id>/actividad/crear/', CrearActividad.as_view(), name="docente_seccion_actividad_crear"),
    path('seccion/<seccion_id>/actividad/<pk>/actualizar/', ActualizarActividad.as_view(), name="docente_seccion_actividad_actualizar"),
    path('seccion/actividad/<pk>/eliminar/', eliminar_actividad, name="docente_seccion_actividad_eliminar"),
    
    path('mantenedor/proyecto/', mantenedor_proyecto, name="mantenedor_proyecto"),
    path('lista/secciones/', lista_secciones, name="lista_secciones"),
    path('lista/alumnos/', lista_alumnos, name="lista_alumnos"),

    path('mantenedor/actividad/', mantenedor_actividades, name="mantenedor_actividades"),
    path('mantenedor/configuracionBase/', mantenedor_configuracionBase, name="mantenedor_configuracionBase"),
]