# -*- coding: utf-8 -*-
from function import ConsultaBD
from function import formatear_error
from django.core.management.commands.migrate import Command as MigrateCommand

import logging
class Command(MigrateCommand):
    def handle(self, *args, **options):
        super().handle(*args, **options)
        try:
            query = """
            --HABILITA EL USO DEL LOCAL HOST
            UPDATE public.django_site SET "domain"='localhost', "name"='localhost' WHERE id=1;
            --USUARIO BASE
            INSERT INTO public.auth_user (id, "password", last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
            VALUES(0, 'pbkdf2_sha256$260000$ZtD3llWxk4uUtbl5ExkvMp$Kz1Z4ByRhrLhoJ1J//UVSrqq0B7ZtZVBvPkUTExUD5Y=', NULL, true, 'automatización', '', '', '', true, true, now());
            --USUARIO ADMINISTRADOR
            INSERT INTO public.auth_user (id, "password", last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
            VALUES(1, '', now(), false, '173733321@ACADEMICOS.uamericas.cl', 'CARLOS', 'MARIN GONZALEZ', 'carlos.marin.gonzalez@edu.udla.cl', true, true, now());
            --DOCENTE
            INSERT INTO public.auth_user (id, "password", last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
            VALUES(2, '', now(), false, '121820897@ACADEMICOS.uamericas.cl', 'JUAN CARLOS', 'SABA SAMUR', 'JSABASAM@EDU.UDLA.CL', true, true, now());
            --ALUMNOS
            INSERT INTO public.auth_user (id, "password", last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
            VALUES(3, '', now(), false, '153702527@ACADEMICOS.uamericas.cl', 'JORGE ANDRES', 'BERRIOS PEREZ', 'Jorge.berrios@edu.udla.cl', true, true, now());
            INSERT INTO public.auth_user (id, "password", last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
            VALUES(4, '', now(), false, '199026860@ACADEMICOS.uamericas.cl', 'CARLOS ANDRES', 'DIAZ RODRÍGUEZ', 'CARLOSANDRES.DIAZ@EDU.UDLA.CL', true, true, now());
            INSERT INTO public.auth_user (id, "password", last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
            VALUES(5, '', now(), false, '213649264@ACADEMICOS.uamericas.cl', 'MARCEL EDUARDO', 'MEDINA PEREZ', 'marcel.medina@edu.udla.cl', true, true, now());
            SELECT setval('auth_user_id_seq',6, true);
            --PARAMETROS BASE PARA TIPO MODULO
            INSERT INTO public.parametro(nombre, metadatos)VALUES('auth_user_auto',cast('{"auth_user_id": "0"}' AS json));
            INSERT INTO public.parametro(nombre, metadatos)VALUES('ACTIVIDADES_BASE_COMPLETA','[{\"nombre\": \"INTRODUCCI\\u00d3N\", \"descripcion\": \"ESTE CAP\\u00cdTULO CONSISTE EN UNA EXPOSICI\\u00d3N BREVE DEL PROBLEMA QUE SE PRETENDE SOLUCIONAR Y/O INVESTIGAR. TODA INFORMACI\\u00d3N DEBER\\u00c1 IR ACOMPA\\u00d1ADA DE LA CORRESPONDIENTE CITA BIBLIOGR\\u00c1FICA, COMO SE INDICA M\\u00c1S ADELANTE. LA INTRODUCCI\\u00d3N TAMBI\\u00c9N DEBE PRESENTAR LA RELEVANCIA DEL PROYECTO O INVESTIGACI\\u00d3N.\", \"tipo_entrada_id\": 1, \"ind_base\": true, \"orden\": 0, \"actividades\": null}, {\"nombre\": \"ASPECTOS DE LA EMPRESA\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"orden\": 1, \"actividades\": [{\"nombre\": \"ANTECEDENTES DE LA EMPRESA\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 1, \"actividades\": null}, {\"nombre\": \"ORGANIGRAMA\", \"descripcion\": \"\", \"tipo_entrada_id\": 4, \"ind_base\": false, \"orden\": 2, \"actividades\": null}, {\"nombre\": \"\\u00c1REA FUNCIONAL\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 3, \"actividades\": null}, {\"nombre\": \"DESCRIPCI\\u00d3N DEL PROCESO A INTERVENIR (BPMN)\", \"descripcion\": \"\", \"tipo_entrada_id\": 4, \"ind_base\": false, \"orden\": 4, \"actividades\": null}]}, {\"nombre\": \"SITUACI\\u00d3N ACTUAL DEL PROYECTO\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"orden\": 2, \"actividades\": [{\"nombre\": \"DESCRIPCI\\u00d3N DE LA SITUACI\\u00d3N ACTUAL\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 1, \"actividades\": null}, {\"nombre\": \"DESCRIPCI\\u00d3N DEL PROBLEMA\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 2, \"actividades\": null}, {\"nombre\": \"PROP\\u00d3SITO DEL PROYECTO\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 3, \"actividades\": null}, {\"nombre\": \"ESTADO DEL ARTE\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 4, \"actividades\": null}, {\"nombre\": \"SOLUCI\\u00d3N PLANTEADA\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 5, \"actividades\": null}, {\"nombre\": \"ALCANCES Y RESTRICCIONES\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 6, \"actividades\": null}]}, {\"nombre\": \"PLANTEAMIENTOS DE OBJETIVOS\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"orden\": 3, \"actividades\": [{\"nombre\": \"GENERAL\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 1, \"actividades\": null}, {\"nombre\": \"ESPEC\\u00cdFICOS\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 2, \"actividades\": null}]}, {\"nombre\": \"ESTUDIO DE FACTIBILIDAD Y GESTI\\u00d3N DE RIESGOS\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"orden\": 4, \"actividades\": [{\"nombre\": \"ESTUDIO DE FACTIBILIDAD\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 1, \"actividades\": [{\"nombre\": \"FACTIBILIDAD T\\u00c9CNICA\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 1}, {\"nombre\": \"AN\\u00c1LISIS COSTO BENEFICIO A UN A\\u00d1O\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"orden\": 2}, {\"nombre\": \"FACTIBILIDAD OPERACIONAL\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 3}, {\"nombre\": \"FACTIBILIDAD LEGAL\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 4}]}, {\"nombre\": \"IDENTIFCACI\\u00d3N DE RIESGOS\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"orden\": 2, \"actividades\": [{\"nombre\": \"RIESGOS DE PLANEACI\\u00d3N\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"orden\": 1}, {\"nombre\": \"RIESGOS DE DESARROLLO\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"orden\": 2}, {\"nombre\": \"RIESGOS DEL CLIENTE\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"orden\": 3}, {\"nombre\": \"RIESGOS DE IMPLEMENTACI\\u00d3N\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"orden\": 4}]}]}, {\"nombre\": \"PLANTEAMIENTO DE LA SOLUCI\\u00d3N\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"orden\": 5, \"actividades\": [{\"nombre\": \"AN\\u00c1LISIS DE LA SOLUCI\\u00d3N\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"orden\": 1, \"actividades\": [{\"nombre\": \"DESCRIPCI\\u00d3N DE LA SOLUCI\\u00d3N PROPUESTA EN DETALLE\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 1}, {\"nombre\": \"EVALUACI\\u00d3N DE HERRAMIENTAS DE DESARROLLO E IMPLEMENTACI\\u00d3N\", \"descripcion\": \"\", \"tipo_entrada_id\": 4, \"ind_base\": false, \"orden\": 2}, {\"nombre\": \"DIAGRAMA DE ARQUITECTURA DE SOLUCI\\u00d3N PROPUESTA\", \"descripcion\": \"\", \"tipo_entrada_id\": 4, \"ind_base\": false, \"orden\": 3}, {\"nombre\": \"DIAGRAMA PROCESO MEJORADO.\", \"descripcion\": \"BPMN\", \"tipo_entrada_id\": 4, \"ind_base\": false, \"orden\": 4}]}, {\"nombre\": \"METODOLOG\\u00cdA APLICADA\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"orden\": 2, \"actividades\": [{\"nombre\": \"COMPARATIVA DE METODOLOG\\u00cdAS ASOCIADAS AL PROYECTO\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"orden\": 1}, {\"nombre\": \"JUSTIFICACI\\u00d3N DE LA METODOLOG\\u00cdA SELECCIONADA\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 2}, {\"nombre\": \"METODOLOG\\u00cdA DE ADMINISTRACI\\u00d3N\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 3}, {\"nombre\": \"CARTA GANTT\", \"descripcion\": \"\", \"tipo_entrada_id\": 4, \"ind_base\": false, \"orden\": 4}]}, {\"nombre\": \"OBTENCI\\u00d3N DE REQUERIMIENTOS\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"orden\": 3, \"actividades\": [{\"nombre\": \"METODOLOG\\u00cdA APLICADA A LA TOMA DE REQUERIMIENTOS\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 1}, {\"nombre\": \"REQUERIMIENTOS FUNCIONALES\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"orden\": 2}, {\"nombre\": \"REQUERIMIENTOS NO FUNCIONALES\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"orden\": 3}, {\"nombre\": \"REQUERIMIENTOS DE SEGURIDAD\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"orden\": 4}, {\"nombre\": \"REQUERIMIENTOS DE MANTENCI\\u00d3N\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"orden\": 5}, {\"nombre\": \"ESPECIFICACI\\u00d3N DE REQUERIMIENTO\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"orden\": 6}]}]}, {\"nombre\": \"DISE\\u00d1O DEL SISTEMA\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"orden\": 6, \"actividades\": [{\"nombre\": \"MODELAMIENTO UML\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"orden\": 1, \"actividades\": [{\"nombre\": \"DIAGRAMA CASOS DE USOS\", \"descripcion\": \"DEBE SER INCLUSI\\u00d3N O EXTENSI\\u00d3N\", \"tipo_entrada_id\": 4, \"ind_base\": false, \"orden\": 1}, {\"nombre\": \"DOCUMENTACI\\u00d3N CASOS DE USO\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"orden\": 2}, {\"nombre\": \"DIAGRAMA DE COMPONENTES\", \"descripcion\": \"\", \"tipo_entrada_id\": 4, \"ind_base\": false, \"orden\": 3}]}, {\"nombre\": \"MODELO ENTIDAD RELACI\\u00d3N O MODELO DE DATOS DEPENDE DEL PROYECTO\", \"descripcion\": \"\", \"tipo_entrada_id\": 4, \"ind_base\": false, \"orden\": 2, \"actividades\": null}]}, {\"nombre\": \"CONSTRUCCI\\u00d3N DE PROTOTIPO FUNCIONAL\", \"descripcion\": \"\", \"tipo_entrada_id\": 4, \"ind_base\": false, \"orden\": 7, \"actividades\": null}, {\"nombre\": \"DISE\\u00d1OS DE PRUEBAS DEL SOFTWARE\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"orden\": 8, \"actividades\": null}, {\"nombre\": \"CONCLUSIONES DEL PROYECTO\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"orden\": 9, \"actividades\": [{\"nombre\": \"CONCLUSIONES\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 1, \"actividades\": null}, {\"nombre\": \"PERSPECTIVAS FUTURAS\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"orden\": 2, \"actividades\": null}]}, {\"nombre\": \"BIBLIOGRAF\\u00cdA (APA)\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": true, \"orden\": 98, \"actividades\": null}, {\"nombre\": \"ANEXOS\", \"descripcion\": \"\", \"tipo_entrada_id\": 3, \"ind_base\": true, \"orden\": 99, \"actividades\": null}]'::jsonb);
            INSERT INTO public.parametro(nombre, metadatos)VALUES('ACTIVIDADES_BASE_MINIMA', '[{\"orden\": 0, \"nombre\": \"INTRODUCCI\\u00d3N\", \"descripcion\": \"ESTE CAP\\u00cdTULO CONSISTE EN UNA EXPOSICI\\u00d3N BREVE DEL PROBLEMA QUE SE PRETENDE SOLUCIONAR Y/O INVESTIGAR. TODA INFORMACI\\u00d3N DEBER\\u00c1 IR ACOMPA\\u00d1ADA DE LA CORRESPONDIENTE CITA BIBLIOGR\\u00c1FICA, COMO SE INDICA M\\u00c1S ADELANTE. LA INTRODUCCI\\u00d3N TAMBI\\u00c9N DEBE PRESENTAR LA RELEVANCIA DEL PROYECTO O INVESTIGACI\\u00d3N.\", \"tipo_entrada\": 1, \"ind_base\": true}, {\"orden\": 98, \"nombre\": \"BIBLIOGRAF\\u00cdA (APA)\", \"descripcion\": \"\", \"tipo_entrada\": 1, \"ind_base\": true}, {\"orden\": 99, \"nombre\": \"ANEXOS\", \"descripcion\": \"\", \"tipo_entrada\": 3, \"ind_base\": true}]'::jsonb);
            --MODULOS
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            values(1,'Inicio','proyecto:home','tf-icons bx bx-home-circle', 0, true, null);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            values(2,'Cambio Perfil','proyecto:cambio_perfil','', 0, false, null);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            values(3,'MANTENEDOR','','tf-icons bx bxs-brightness', 4, true, null);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            values(4,'USUARIO','proyecto:mantenedor_usuario','', 1, true, 3);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            values(5,'Impersonar','proyecto:impersonar_usuario','', 0, false, null);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(6,'sección', 'proyecto:mantenedor_secciones', 'tf-icons bx bxs-factory',2, true, 3);
            INSERT INTO public.modulo(id, nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(10, 'Mis secciones', 'proyecto:alumno_secciones', 'tf-icons bx bxs-factory', 5, true, null);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(11,'Mis secciones', 'proyecto:docente_secciones', 'tf-icons bx bxs-factory',1, true, null);
            INSERT INTO public.modulo(id, nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(12, 'Administrar alumnos', 'proyecto:lista_alumnos', 'tf-icons bx bxs-factory', 0, false, NULL);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(13,'semestre', 'proyecto:mantenedor_semestre', 'tf-icons bx bxs-factory',2, true, 3);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(14,'Docente actividades sección', 'proyecto:docente_seccion_actividades', 'tf-icons bx bxs-factory',2, false, null);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(15,'Crear actividad', 'proyecto:docente_seccion_actividad_crear', 'tf-icons bx bxs-factory',3, false, null);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(16,'Actualizar actividad', 'proyecto:docente_seccion_actividad_actualizar', 'tf-icons bx bxs-factory',4, false, null);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(17,'Eliminar actividad', 'proyecto:docente_seccion_actividad_eliminar', 'tf-icons bx bxs-factory',5, false, null);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(18,'Crear usuario', 'proyecto:mantenedor_usuario_crear', 'tf-icons bx bxs-factory',6, false, null);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(19,'Actualizar usuario', 'proyecto:mantenedor_usuario_actualizar', 'tf-icons bx bxs-factory',7, false, null);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(20,'Buscador de usuarios', 'proyecto:mantenedor_usuario_buscar', 'tf-icons bx bxs-factory',8, false, null);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(21,'Eliminar Seccion', 'proyecto:mantenedor_seccion_eliminar', 'tf-icons bx bxs-factory',10, false, null);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(22,'Actualizar Seccion', 'proyecto:mantenedor_seccion_actualizar', 'tf-icons bx bxs-factory',11, false, null);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(23,'Administrar Seccion', 'proyecto:mantenedor_seccion_administar', 'tf-icons bx bxs-factory',12, false, null);
            INSERT INTO public.modulo(id, nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(24, 'Docente participantes sección', 'proyecto:docente_seccion_participantes', 'tf-icons bx bxs-factory', 13, false, NULL);
            INSERT INTO public.modulo(id, nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(25, 'Crear proyecto', 'proyecto:alumno_seccion_proyecto_crear', 'tf-icons bx bxs-factory', 14, false, NULL);
            INSERT INTO public.modulo(id, nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(26, 'cambiar estado proyecto', 'proyecto:docente_proyecto_estado', 'tf-icons bx bxs-factory', 15, false, NULL);
            --PERFIL
            INSERT INTO public.perfil(id,nombre,ind_asignable)VALUES(1,'ADMINISTRADOR',true);
            INSERT INTO public.perfil(id,nombre,ind_asignable)VALUES(2,'PROFESOR',true);
            INSERT INTO public.perfil(id,nombre,ind_asignable)VALUES(3,'ALUMNO',true);
            INSERT INTO public.perfil(id,nombre,ind_asignable)VALUES(4,'INVITADO',false);
            SELECT setval('perfil_id_seq',5, true);
            --PARAMETRO PERFIL INVITADO
            INSERT INTO public.parametro(nombre,metadatos)VALUES('perfil_invitado',cast('{"perfil_id": "4"}' AS json));
            --PERFIL ACTIVO USUARIO ADMINISTRADOR
            INSERT INTO public.usuario_perfil_activo(fecha, perfil_id, responsable_id, usuario_id)VALUES(now(),1, 0, 1);
            --PERFIL ACTIVO USUARIO DOCENTE
            INSERT INTO public.usuario_perfil_activo(fecha, perfil_id, responsable_id, usuario_id)VALUES(now(),2, 0, 2);
            --PERFIL ACTIVO USUARIOS ALUMNOS
            INSERT INTO public.usuario_perfil_activo(fecha, perfil_id, responsable_id, usuario_id)VALUES(now(),3, 0, 3);
            INSERT INTO public.usuario_perfil_activo(fecha, perfil_id, responsable_id, usuario_id)VALUES(now(),3, 0, 4);
            INSERT INTO public.usuario_perfil_activo(fecha, perfil_id, responsable_id, usuario_id)VALUES(now(),3, 0, 5);
            --PERMISOS POR PERFIL
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(1,1,1);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(2,1,2);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(3,1,3);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(4,1,4);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(5,2,1);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(6,2,2);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(7,2,3);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(8,3,1);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(10,4,1);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(11,5,1);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(14,6,1);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(16,10,3);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(17,11,2);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(18,12,2);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(19,14,2);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(20,15,2);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(21,16,2);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(22,17,2);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(23,18,1);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(24,19,1);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(25,20,1);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(26,21,1);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(27,22,1);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(28,23,1);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(29,24,2);
            INSERT INTO public.perfil_modulo(id, modulo_id,perfil_id)VALUES(30,25,3);
            INSERT INTO public.perfil_modulo(id, modulo_id,perfil_id)VALUES(31,26,2);
            --ACCESSO USUARIO DEMO
            INSERT INTO public.perfil_usuario(fecha, perfil_id, responsable_id, usuario_id)VALUES(now(),1,0,1);
            INSERT INTO public.perfil_usuario(fecha, perfil_id, responsable_id, usuario_id)VALUES(now(),2,0,2);
            INSERT INTO public.perfil_usuario(fecha, perfil_id, responsable_id, usuario_id)VALUES(now(),3,0,2);
            INSERT INTO public.perfil_usuario(fecha, perfil_id, responsable_id, usuario_id)VALUES(now(),3,0,3);
            INSERT INTO public.perfil_usuario(fecha, perfil_id, responsable_id, usuario_id)VALUES(now(),3,0,4);
            INSERT INTO public.perfil_usuario(fecha, perfil_id, responsable_id, usuario_id)VALUES(now(),3,0,5);
            -- SP PERMISOS MODULO USUARIO
            CREATE OR REPLACE FUNCTION public.sp_web_get_permisos_modulo_usuario(p_usuario_id int4)
            RETURNS TABLE(perfil_activo text,cantidad_perfiles int4,modulos json)
            LANGUAGE plpgsql
            AS $function$BEGIN
            RETURN QUERY 	 
            select T2.nombre as perfil_activo,(
                select count(distinct p1.perfil_id) from public.perfil_usuario p1
                where p1.usuario_id = t1.usuario_id and p1.perfil_id::int4 != (
                    SELECT (pa1.metadatos::jsonb->>'perfil_id')::int4 FROM public.parametro pa1 WHERE pa1.nombre='perfil_invitado' limit 1
                )::int4
            )::int4 as cantidad_perfiles,(
                select to_json(array_agg(row_to_json(listado_modulos))) from (
                    select initcap(m3.nombre) as nombre, m3.url,m3.icono,m3.ind_url as is_url,m3.orden,(
                        select to_json(array_agg(row_to_json(listado_submodulos))) from (
                            select initcap(s3.nombre) as nombre, s3.url,s3.icono,s3.ind_url as is_url,s3.orden
                            from public.perfil_usuario s1
                            inner join public.perfil_modulo s2 on s1.perfil_id = s2.perfil_id
                            inner join public.modulo s3 on s2.modulo_id = s3.id
                            where s1.usuario_id = t1.usuario_id and s1.perfil_id = t1.perfil_id and s3.modulo_padre_id = m2.modulo_id
                            order by s3.orden
                        ) listado_submodulos
                    ) as submodulos
                    from public.perfil_usuario m1
                    inner join public.perfil_modulo m2 on m1.perfil_id = m2.perfil_id
                    inner join public.modulo m3 on m2.modulo_id = m3.id
                    where m1.usuario_id = t1.usuario_id and m1.perfil_id = t1.perfil_id and m3.modulo_padre_id is null
                    order by m3.orden 
                ) listado_modulos
            ) as modulos
            from public.usuario_perfil_activo t1
            inner join public.perfil t2 on t1.perfil_id = t2.id
            where t1.usuario_id = p_usuario_id;
            END;$function$
            ;
            --SEMESTRES
            INSERT INTO public.semestre (id,nombre) values (1,'PRIMER SEMESTRE');
            INSERT INTO public.semestre (id,nombre) values (2,'SEGUNDO SEMESTRE');
            --SECCIONES
            INSERT INTO public.seccion(id, codigo, fecha_desde, fecha_hasta, fecha, responsable_id, semestre_id) VALUES
            (1, 'ACI594-480', '2023-02-28 21:00:00.000', '2023-07-30 20:00:00.000', '2023-02-05 17:32:13.234', 1, 1);
            SELECT setval('seccion_id_seq',2, true);
            --alumno seccion
            INSERT INTO public.alumno_seccion(id, fecha, responsable_id, seccion_id, usuario_id)VALUES(1, now(), 1, 1, 3);
            INSERT INTO public.alumno_seccion(id, fecha, responsable_id, seccion_id, usuario_id)VALUES(2, now(), 1, 1, 4);
            INSERT INTO public.alumno_seccion(id, fecha, responsable_id, seccion_id, usuario_id)VALUES(3, now(), 1, 1, 2);
            SELECT setval('alumno_seccion_id_seq',4, true);
            --docente seccion
            INSERT INTO public.docente_seccion(id, fecha, responsable_id, seccion_id, usuario_id)VALUES(1, now(), 1, 1, 2);
            SELECT setval('docente_seccion_id_seq',2, true);
            --tipos dato
            INSERT INTO public.tipo_entrada(id, nombre, tipo, ind_archivo, ind_multiple, formato, fecha, responsable_id)VALUES(1, 'PARRAFO', 'textarea', false, false, NULL, '2023-03-01 11:40:14.538', 0);
            INSERT INTO public.tipo_entrada(id, nombre, tipo, ind_archivo, ind_multiple, formato, fecha, responsable_id)VALUES(2, 'TABLA', 'file', true, true, 'jpeg', '2023-03-01 11:40:14.538', 0);
            INSERT INTO public.tipo_entrada(id, nombre, tipo, ind_archivo, ind_multiple, formato, fecha, responsable_id)VALUES(3, 'PDF', 'file', true, true, 'pdf', '2023-03-01 11:40:14.538', 0);
            INSERT INTO public.tipo_entrada(id, nombre, tipo, ind_archivo, ind_multiple, formato, fecha, responsable_id)VALUES(4, 'FIGURA', 'file', true, true, 'jpeg', '2023-03-01 11:40:14.538', 0);
            SELECT setval('tipo_entrada_id_seq',3, true);
            --actividades
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(106, 'DIAGRAMA PROCESO MEJORADO.', 'BPMN', false, 4, '2023-03-04 01:05:58.663', 31, 2, 1, 4);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(105, 'EVALUACIÓN DE HERRAMIENTAS DE DESARROLLO E IMPLEMENTACIÓN', '', false, 2, '2023-03-04 01:04:09.950', 31, 2, 1, 4);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(58, 'PERSPECTIVAS FUTURAS', '', false, 2, '2023-02-28 19:53:03.082', 56, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(57, 'CONCLUSIONES', '', false, 1, '2023-02-28 19:52:32.663', 56, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(56, 'CONCLUSIONES DEL PROYECTO', '', false, 9, '2023-02-28 19:51:51.215', NULL, 2, 1, NULL);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(55, 'DISEÑOS DE PRUEBAS DEL SOFTWARE', '', false, 8, '2023-02-28 19:51:26.315', NULL, 2, 1, 2);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(54, 'MODELO ENTIDAD RELACIÓN O MODELO DE DATOS DEPENDE DEL PROYECTO', '', false, 2, '2023-02-28 19:50:18.882', 48, 2, 1, 4);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(53, 'CONSTRUCCIÓN DE PROTOTIPO FUNCIONAL', '', false, 7, '2023-02-28 19:49:27.219', NULL, 2, 1, 4);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(52, 'DIAGRAMA DE COMPONENTES', '', false, 3, '2023-02-28 19:45:51.424', 49, 2, 1, 4);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(51, 'DOCUMENTACIÓN CASOS DE USO', '', false, 2, '2023-02-28 19:45:26.241', 49, 2, 1, 2);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(50, 'DIAGRAMA CASOS DE USOS', 'DEBE SER INCLUSIÓN O EXTENSIÓN', false, 1, '2023-02-28 19:44:47.063', 49, 2, 1, 4);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(49, 'MODELAMIENTO UML', '', false, 1, '2023-02-28 19:43:49.186', 48, 2, 1, NULL);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(48, 'DISEÑO DEL SISTEMA', '', false, 6, '2023-02-28 19:43:19.725', NULL, 2, 1, NULL);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(47, 'ESPECIFICACIÓN DE REQUERIMIENTO', '', false, 6, '2023-02-28 19:42:59.092', 41, 2, 1, 2);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(46, 'REQUERIMIENTOS DE MANTENCIÓN', '', false, 5, '2023-02-28 19:42:20.300', 41, 2, 1, 2);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(45, 'REQUERIMIENTOS DE SEGURIDAD', '', false, 4, '2023-02-28 19:41:51.002', 41, 2, 1, 2);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(44, 'REQUERIMIENTOS NO FUNCIONALES', '', false, 3, '2023-02-28 19:41:22.361', 41, 2, 1, 2);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(43, 'REQUERIMIENTOS FUNCIONALES', '', false, 2, '2023-02-28 19:40:46.597', 41, 2, 1, 2);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(42, 'METODOLOGÍA APLICADA A LA TOMA DE REQUERIMIENTOS', '', false, 1, '2023-02-28 19:40:22.286', 41, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(41, 'OBTENCIÓN DE REQUERIMIENTOS', '', false, 3, '2023-02-28 19:39:36.957', 30, 2, 1, NULL);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(40, 'CARTA GANTT', '', false, 4, '2023-02-28 19:38:59.153', 36, 2, 1, 4);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(39, 'METODOLOGÍA DE ADMINISTRACIÓN', '', false, 3, '2023-02-28 19:38:31.960', 36, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(38, 'JUSTIFICACIÓN DE LA METODOLOGÍA SELECCIONADA', '', false, 2, '2023-02-28 19:38:05.780', 36, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(37, 'COMPARATIVA DE METODOLOGÍAS ASOCIADAS AL PROYECTO', '', false, 1, '2023-02-28 19:37:22.909', 36, 2, 1, 2);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(36, 'METODOLOGÍA APLICADA', '', false, 2, '2023-02-28 19:36:35.291', 30, 2, 1, NULL);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(34, 'DIAGRAMA DE ARQUITECTURA DE SOLUCIÓN PROPUESTA', '', false, 3, '2023-02-28 19:35:41.260', 31, 2, 1, 4);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(32, 'DESCRIPCIÓN DE LA SOLUCIÓN PROPUESTA EN DETALLE', '', false, 1, '2023-02-28 19:34:18.568', 31, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(31, 'ANÁLISIS DE LA SOLUCIÓN', '', false, 1, '2023-02-28 19:33:41.795', 30, 2, 1, NULL);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(30, 'PLANTEAMIENTO DE LA SOLUCIÓN', '', false, 5, '2023-02-28 19:33:13.797', NULL, 2, 1, NULL);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(29, 'RIESGOS DE IMPLEMENTACIÓN', '', false, 4, '2023-02-28 19:32:38.428', 25, 2, 1, 2);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(28, 'RIESGOS DEL CLIENTE', '', false, 3, '2023-02-28 19:32:06.483', 25, 2, 1, 2);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(27, 'RIESGOS DE DESARROLLO', '', false, 2, '2023-02-28 19:31:46.313', 25, 2, 1, 2);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(26, 'RIESGOS DE PLANEACIÓN', '', false, 1, '2023-02-28 19:31:14.897', 25, 2, 1, 2);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(25, 'IDENTIFCACIÓN DE RIESGOS', '', false, 2, '2023-02-28 19:30:48.106', 19, 2, 1, NULL);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(24, 'FACTIBILIDAD LEGAL', '', false, 4, '2023-02-28 19:30:15.036', 20, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(23, 'FACTIBILIDAD OPERACIONAL', '', false, 3, '2023-02-28 19:29:50.007', 20, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(22, 'ANÁLISIS COSTO BENEFICIO A UN AÑO', '', false, 2, '2023-02-28 19:29:19.778', 20, 2, 1, 2);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(21, 'FACTIBILIDAD TÉCNICA', '', false, 1, '2023-02-28 19:28:35.274', 20, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(20, 'ESTUDIO DE FACTIBILIDAD', '', false, 1, '2023-02-28 19:28:06.647', 19, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(19, 'ESTUDIO DE FACTIBILIDAD Y GESTIÓN DE RIESGOS', '', false, 4, '2023-02-28 19:27:30.306', NULL, 2, 1, NULL);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(18, 'ESPECÍFICOS', '', false, 2, '2023-02-28 19:26:45.269', 16, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(17, 'GENERAL', '', false, 1, '2023-02-28 19:26:21.583', 16, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(16, 'PLANTEAMIENTOS DE OBJETIVOS', '', false, 3, '2023-02-28 19:26:02.754', NULL, 2, 1, NULL);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(15, 'ALCANCES Y RESTRICCIONES', '', false, 6, '2023-02-28 19:25:38.526', 9, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(14, 'SOLUCIÓN PLANTEADA', '', false, 5, '2023-02-28 19:25:12.962', 9, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(13, 'ESTADO DEL ARTE', '', false, 4, '2023-02-28 19:24:44.501', 9, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(12, 'PROPÓSITO DEL PROYECTO', '', false, 3, '2023-02-28 19:24:21.390', 9, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(11, 'DESCRIPCIÓN DEL PROBLEMA', '', false, 2, '2023-02-28 19:23:56.618', 9, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(10, 'DESCRIPCIÓN DE LA SITUACIÓN ACTUAL', '', false, 1, '2023-02-28 19:23:27.304', 9, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(9, 'SITUACIÓN ACTUAL DEL PROYECTO', '', false, 2, '2023-02-28 19:22:40.455', NULL, 2, 1, NULL);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(8, 'DESCRIPCIÓN DEL PROCESO A INTERVENIR (BPMN)', '', false, 4, '2023-02-28 19:22:13.332', 4, 2, 1, 4);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(7, 'ÁREA FUNCIONAL', '', false, 3, '2023-02-28 19:21:36.040', 4, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(6, 'ORGANIGRAMA', '', false, 2, '2023-02-28 19:21:13.501', 4, 2, 1, 4);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(5, 'ANTECEDENTES DE LA EMPRESA', '', false, 1, '2023-02-28 19:20:32.429', 4, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(4, 'ASPECTOS DE LA EMPRESA', '', false, 1, '2023-02-28 19:15:37.484', NULL, 2, 1, NULL);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(3, 'ANEXOS', '', true, 99, '2023-02-28 19:54:57.634', NULL, 2, 1, 3);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(2, 'BIBLIOGRAFÍA (APA)', '', true, 98, '2023-02-28 19:53:44.267', NULL, 2, 1, 1);
            INSERT INTO public.actividad(id, nombre, descripcion, ind_base, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(1, 'INTRODUCCIÓN', 'ESTE CAPÍTULO CONSISTE EN UNA EXPOSICIÓN BREVE DEL PROBLEMA QUE SE PRETENDE SOLUCIONAR Y/O INVESTIGAR. TODA INFORMACIÓN DEBERÁ IR ACOMPAÑADA DE LA CORRESPONDIENTE CITA BIBLIOGRÁFICA, COMO SE INDICA MÁS ADELANTE. LA INTRODUCCIÓN TAMBIÉN DEBE PRESENTAR LA RELEVANCIA DEL PROYECTO O INVESTIGACIÓN.', true, 0, '2023-02-26 19:55:20.145', NULL, 2, 1, 1);
            SELECT setval('actividad_id_seq',107, true);
            """
            demo_descripcion = "LOREM IPSUM IS SIMPLY DUMMY TEXT OF THE PRINTING AND TYPESETTING INDUSTRY. LOREM IPSUM HAS BEEN THE INDUSTRY''S STANDARD DUMMY TEXT EVER SINCE THE 1500S, WHEN AN UNKNOWN PRINTER TOOK A GALLEY OF TYPE AND SCRAMBLED IT TO MAKE A TYPE SPECIMEN BOOK. IT HAS SURVIVED NOT ONLY FIVE CENTURIES, BUT ALSO THE LEAP INTO ELECTRONIC TYPESETTING, REMAINING ESSENTIALLY UNCHANGED. IT WAS POPULARISED IN THE 1960S WITH THE RELEASE OF LETRASET SHEETS CONTAINING LOREM IPSUM PASSAGES, AND MORE RECENTLY WITH DESKTOP PUBLISHING SOFTWARE LIKE ALDUS PAGEMAKER INCLUDING VERSIONS OF LOREM IPSUM."
            # demo_descripcion = demo_descripcion.encode(encoding='ascii',errors='backslashreplace')
            query += f"""--proyecto demo
            INSERT INTO public.proyecto(id, nombre, descripcion, ind_aprobado, in_activo, motivo_rechazo, fecha_desde, fecha_hasta, fecha, alumno_seccion_id, responsable_id)
            VALUES(1, 'PROYECTO PRUEBA 1', '{demo_descripcion}', true, true, NULL, '2023-02-28 21:00:00.000', '2023-08-30 20:00:00.000', '2023-03-04 00:04:49.683', 3, 2);    
            SELECT setval('proyecto_id_seq',2, true);"""
            ConsultaBD(query).execute_lines()
        except Exception as exc:
            logging.warning(formatear_error(exc))
            print(formatear_error(exc))