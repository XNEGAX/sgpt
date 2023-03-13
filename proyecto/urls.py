from django.urls import path
from rest_framework.routers import DefaultRouter

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
from proyecto.views.mantenedor import EliminarSeccion
from proyecto.views.mantenedor import AdministrarSeccion

from proyecto.views.docente import MantenedorSeccionesDocente
from proyecto.views.docente import ListarParticipantes
from proyecto.views.docente import MantenedorActividad
from proyecto.views.docente import CrearActividad
from proyecto.views.docente import ActualizarActividad
from proyecto.views.docente import EliminarActividad
from proyecto.views.docente import ProyectoActualizar

from proyecto.views.alumno import ListarSeccionesAlumno
from proyecto.views.alumno import CrearProyectoTitulo
from proyecto.views.alumno import ActualizarProyectoTitulo
from proyecto.views.alumno import ResponderActvidades

from proyecto.views.alumno import CrearTareaProyecto
from proyecto.views.alumno import ActualizaTareaProyecto
from proyecto.views.alumno import EliminarTareaProyecto
from proyecto.views.alumno import EliminarArchivoActividad
from proyecto.views.alumno import ListarBitacora
from proyecto.views.alumno import InformeTituloView

from proyecto.views.docente import DetalleAlumnoProyecto

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
    path('mantenedor/seccion/<pk>/eliminar/', EliminarSeccion.as_view(), name="mantenedor_seccion_eliminar"),
    path('mantenedor/seccion/<pk>/administrar/', AdministrarSeccion.as_view(), name="mantenedor_seccion_administar"),
    path('mantenedor/seccion/<pk>/<metodo>/<perfil>/', AdministrarSeccion.as_view(), name="mantenedor_seccion_administar"),
    path('mantenedor/seccion/<pk>/<metodo>/<perfil>/<usuario>/', AdministrarSeccion.as_view(), name="mantenedor_seccion_administar"),

    path('docente/secciones/', MantenedorSeccionesDocente.as_view(), name="docente_secciones"),
    path('docente/seccion/<seccion_id>/participantes/', ListarParticipantes.as_view(), name="docente_seccion_participantes"),
    path('docente/seccion/<seccion_id>/actividades/', MantenedorActividad.as_view(), name="docente_seccion_actividades"),
    path('docente/seccion/<seccion_id>/actividad/crear/', CrearActividad.as_view(), name="docente_seccion_actividad_crear"),
    path('seccion/<seccion_id>/actividad/<pk>/actualizar/', ActualizarActividad.as_view(), name="docente_seccion_actividad_actualizar"),
    path('seccion/actividad/<pk>/eliminar/', EliminarActividad.as_view(), name="docente_seccion_actividad_eliminar"),
    path('docente/proyecto/<pk>/estado/', ProyectoActualizar.as_view(), name="docente_proyecto_estado"),
    
    path('alumno/secciones/', ListarSeccionesAlumno.as_view(), name="alumno_secciones"),
    path('alumno/seccion/<alumno_seccion_id>/proyecto/crear/', CrearProyectoTitulo.as_view(), name="alumno_seccion_proyecto_crear"),
    path('alumno/seccion/proyecto/<pk>/actualizar/', ActualizarProyectoTitulo.as_view(), name="alumno_seccion_proyecto_actualizar"),
    path('alumno/seccion/proyecto/<proyecto_id>/actividades/', ResponderActvidades.as_view(), name="alumno_seccion_actividades"),

    path('alumno/proyecto/<proyecto_id>/tarea/crear/', CrearTareaProyecto.as_view(), name="alumno_proyecto_tarea_crear"),
    path('alumno/proyecto/tarea/<pk>/actualizar/', ActualizaTareaProyecto.as_view(), name="alumno_proyecto_tarea_actualizar"),
    path('alumno/proyecto/tarea/<pk>/eliminar/', EliminarTareaProyecto.as_view(), name="alumno_proyecto_tarea_eliminar"),
    path('alumno/proyecto/<proyecto_id>/actividad/<actividad_id>/archivo/eliminar/', EliminarArchivoActividad.as_view(), name="alumno_proyecto_archivo_eliminar"),
    path('alumno/proyecto/<proyecto_id>/actividad/<actividad_id>/bitacora/listar/', ListarBitacora.as_view(), name="alumno_proyecto_bitacora_listar"),
    
    path('proyecto/<pk>/informe/', InformeTituloView.as_view(), name="proyecto_informe"),

    path('proyecto/<proyecto_id>/informe/detalle/', DetalleAlumnoProyecto.as_view(), name="alumno_proyecto_detalle"),

]
