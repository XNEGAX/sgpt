from function import ConsultaBD
from function import formatear_error
from django.core.management.commands.migrate import Command as MigrateCommand

import logging
class Command(MigrateCommand):
    def handle(self, *args, **options):
        super().handle(*args, **options)
        try:
            ConsultaBD("""
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
            INSERT INTO public.parametro(nombre, metadatos) VALUES('ACTIVIDADES_BASE_COMPLETA', '[{\"orden\": 0, \"nombre\": \"INTRODUCCI\\u00d3N\", \"descripcion\": \"ESTE CAP\\u00cdTULO CONSISTE EN UNA EXPOSICI\\u00d3N BREVE DEL PROBLEMA QUE SE PRETENDE SOLUCIONAR Y/O INVESTIGAR. TODA INFORMACI\\u00d3N DEBER\\u00c1 IR ACOMPA\\u00d1ADA DE LA CORRESPONDIENTE CITA BIBLIOGR\\u00c1FICA, COMO SE INDICA M\\u00c1S ADELANTE. LA INTRODUCCI\\u00d3N TAMBI\\u00c9N DEBE PRESENTAR LA RELEVANCIA DEL PROYECTO O INVESTIGACI\\u00d3N.\", \"tipo_entrada_id\": 1, \"ind_base\": true, \"actividades\": null}, {\"orden\": 1, \"nombre\": \"ASPECTOS DE LA EMPRESA\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"actividades\": [{\"orden\": 1, \"nombre\": \"ANTECEDENTES DE LA EMPRESA\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"actividades\": null}, {\"orden\": 2, \"nombre\": \"ORGANIGRAMA\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"actividades\": null}, {\"orden\": 3, \"nombre\": \"\\u00c1REA FUNCIONAL\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"actividades\": null}, {\"orden\": 4, \"nombre\": \"DESCRIPCI\\u00d3N DEL PROCESO A INTERVENIR (BPMN)\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"actividades\": null}]}, {\"orden\": 2, \"nombre\": \"SITUACI\\u00d3N ACTUAL DEL PROYECTO\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"actividades\": [{\"orden\": 1, \"nombre\": \"DESCRIPCI\\u00d3N DE LA SITUACI\\u00d3N ACTUAL\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"actividades\": null}, {\"orden\": 2, \"nombre\": \"DESCRIPCI\\u00d3N DEL PROBLEMA\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"actividades\": null}, {\"orden\": 3, \"nombre\": \"PROP\\u00d3SITO DEL PROYECTO\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"actividades\": null}, {\"orden\": 4, \"nombre\": \"ESTADO DEL ARTE\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"actividades\": null}, {\"orden\": 5, \"nombre\": \"SOLUCI\\u00d3N PLANTEADA\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"actividades\": null}, {\"orden\": 6, \"nombre\": \"ALCANCES Y RESTRICCIONES\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"actividades\": [{\"orden\": 1, \"nombre\": \"GENERAL\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false}, {\"orden\": 2, \"nombre\": \"ESPEC\\u00cdFICOS\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false}]}]}, {\"orden\": 3, \"nombre\": \"PLANTEAMIENTOS DE OBJETIVOS\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"actividades\": null}, {\"orden\": 4, \"nombre\": \"ESTUDIO DE FACTIBILIDAD Y GESTI\\u00d3N DE RIESGOS\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"actividades\": [{\"orden\": 1, \"nombre\": \"FACTIBILIDAD T\\u00c9CNICA\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"actividades\": null}, {\"orden\": 2, \"nombre\": \"AN\\u00c1LISIS COSTO BENEFICIO A UN A\\u00d1O\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"actividades\": null}, {\"orden\": 3, \"nombre\": \"FACTIBILIDAD OPERACIONAL\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"actividades\": null}, {\"orden\": 4, \"nombre\": \"FACTIBILIDAD LEGAL\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"actividades\": [{\"orden\": 1, \"nombre\": \"RIESGOS DE PLANEACI\\u00d3N\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false}, {\"orden\": 2, \"nombre\": \"RIESGOS DE DESARROLLO\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false}, {\"orden\": 3, \"nombre\": \"RIESGOS DEL CLIENTE\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false}, {\"orden\": 4, \"nombre\": \"RIESGOS DE IMPLEMENTACI\\u00d3N\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false}]}]}, {\"orden\": 5, \"nombre\": \"PLANTEAMIENTO DE LA SOLUCI\\u00d3N\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"actividades\": [{\"orden\": 1, \"nombre\": \"DESCRIPCI\\u00d3N DE LA SOLUCI\\u00d3N PROPUESTA EN DETALLE\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"actividades\": null}, {\"orden\": 2, \"nombre\": \"EVALUACI\\u00d3N DE HERRRAMIENTAS DE DESARROLLO E IMPLEMENTACI\\u00d3N\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"actividades\": null}, {\"orden\": 3, \"nombre\": \"DIAGRAMA DE ARQUITECTURA DE SOLUCI\\u00d3N PROPUESTA EN DETALLE\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"actividades\": null}, {\"orden\": 4, \"nombre\": \"DIAGRAMA PROCESO MEJORADO (BPMN)\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"actividades\": [{\"orden\": 1, \"nombre\": \"COMPARATIVA DE METODOLOG\\u00cdAS ASOCIADAS AL PROYECTO\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false}, {\"orden\": 2, \"nombre\": \"JUSTIFICACI\\u00d3N DE LA METODOLOG\\u00cdA SELECCIONADA\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false}, {\"orden\": 3, \"nombre\": \"METODOLOG\\u00cdA DE ADMINISTRACI\\u00d3N\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false}, {\"orden\": 4, \"nombre\": \"CARTA GANTT\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false}]}]}, {\"orden\": 6, \"nombre\": \"DISE\\u00d1O DEL SISTEMA\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"actividades\": [{\"orden\": 1, \"nombre\": \"DIAGRAMA CASOS DE USOS (DEBE SER INCLUSI\\u00d3N O EXTENSI\\u00d3N)\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"actividades\": null}, {\"orden\": 2, \"nombre\": \"DOCUMENTACI\\u00d3N CASOS DE USO\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"actividades\": null}, {\"orden\": 3, \"nombre\": \"DIAGRAMA DE COMPONENTES\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"actividades\": null}]}, {\"orden\": 7, \"nombre\": \"CONSTRUCCI\\u00d3N DE PROTOTIPO FUNCIONAL\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"actividades\": null}, {\"orden\": 8, \"nombre\": \"DISE\\u00d1OS DE PRUEBAS DEL SOFTWARE\", \"descripcion\": \"\", \"tipo_entrada_id\": 2, \"ind_base\": false, \"actividades\": [{\"orden\": 1, \"nombre\": \"CONCLUSIONES\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"actividades\": null}, {\"orden\": 2, \"nombre\": \"PERSPECTIVAS FUTURAS\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": false, \"actividades\": null}]}, {\"orden\": 9, \"nombre\": \"CONCLUSIONES DEL PROYECTO\", \"descripcion\": \"\", \"tipo_entrada_id\": null, \"ind_base\": false, \"actividades\": null}, {\"orden\": 98, \"nombre\": \"BIBLIOGRAF\\u00cdA (APA)\", \"descripcion\": \"\", \"tipo_entrada_id\": 1, \"ind_base\": true, \"actividades\": null}, {\"orden\": 99, \"nombre\": \"ANEXOS\", \"descripcion\": \"\", \"tipo_entrada_id\": 3, \"ind_base\": true, \"actividades\": null}]'::jsonb);
            INSERT INTO public.parametro(nombre, metadatos) VALUES('ACTIVIDADES_BASE_MINIMA', '[{\"orden\": 0, \"nombre\": \"INTRODUCCI\\u00d3N\", \"descripcion\": \"ESTE CAP\\u00cdTULO CONSISTE EN UNA EXPOSICI\\u00d3N BREVE DEL PROBLEMA QUE SE PRETENDE SOLUCIONAR Y/O INVESTIGAR. TODA INFORMACI\\u00d3N DEBER\\u00c1 IR ACOMPA\\u00d1ADA DE LA CORRESPONDIENTE CITA BIBLIOGR\\u00c1FICA, COMO SE INDICA M\\u00c1S ADELANTE. LA INTRODUCCI\\u00d3N TAMBI\\u00c9N DEBE PRESENTAR LA RELEVANCIA DEL PROYECTO O INVESTIGACI\\u00d3N.\", \"tipo_entrada\": 1, \"ind_base\": true}, {\"orden\": 98, \"nombre\": \"BIBLIOGRAF\\u00cdA (APA)\", \"descripcion\": \"\", \"tipo_entrada\": 1, \"ind_base\": true}, {\"orden\": 99, \"nombre\": \"ANEXOS\", \"descripcion\": \"\", \"tipo_entrada\": 3, \"ind_base\": true}]'::jsonb);
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
            INSERT INTO public.modulo
            (id, nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(24, 'Docente participantes sección', 'proyecto:docente_seccion_participantes', 'tf-icons bx bxs-factory', 13, false, NULL);
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
            INSERT INTO public.tipo_entrada(id, nombre, tipo, ind_archivo, ind_multiple, formato, fecha, responsable_id)VALUES(2, 'IMAGEN', 'file', true, true, 'jpeg', '2023-03-01 11:40:14.538', 0);
            INSERT INTO public.tipo_entrada(id, nombre, tipo, ind_archivo, ind_multiple, formato, fecha, responsable_id)VALUES(3, 'PDF', 'file', true, true, 'pdf', '2023-03-01 11:40:14.538', 0);
            SELECT setval('tipo_entrada_id_seq',3, true);
            --actividades
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(1, 'INTRODUCCIÓN', 'ESTE CAPÍTULO CONSISTE EN UNA EXPOSICIÓN BREVE DEL PROBLEMA QUE SE PRETENDE SOLUCIONAR Y/O INVESTIGAR. TODA INFORMACIÓN DEBERÁ IR ACOMPAÑADA DE LA CORRESPONDIENTE CITA BIBLIOGRÁFICA, COMO SE INDICA MÁS ADELANTE. LA INTRODUCCIÓN TAMBIÉN DEBE PRESENTAR LA RELEVANCIA DEL PROYECTO O INVESTIGACIÓN.', 0, '2023-02-26 22:55:20.145', NULL, 2, 1, 1, true);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(2, 'BIBLIOGRAFÍA (APA)', '', 98, '2023-02-28 22:53:44.267', NULL, 2, 1, 1, true);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(3, 'ANEXOS', '', 99, '2023-02-28 22:54:57.634', NULL, 2, 1, NULL, true);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(4, 'ASPECTOS DE LA EMPRESA', '', 1, '2023-02-28 22:15:37.484', NULL, 2, 1, NULL, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(5, 'ANTECEDENTES DE LA EMPRESA', '', 1, '2023-02-28 22:20:32.429', 4, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(6, 'ORGANIGRAMA', '', 2, '2023-02-28 22:21:13.501', 4, 2, 1, 2, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(7, 'ÁREA FUNCIONAL', '', 3, '2023-02-28 22:21:36.040', 4, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(8, 'DESCRIPCIÓN DEL PROCESO A INTERVENIR (BPMN)', '', 4, '2023-02-28 22:22:13.332', 4, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(9, 'SITUACIÓN ACTUAL DEL PROYECTO', '', 2, '2023-02-28 22:22:40.455', NULL, 2, 1, NULL, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(10, 'DESCRIPCIÓN DE LA SITUACIÓN ACTUAL', '', 1, '2023-02-28 22:23:27.304', 9, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(11, 'DESCRIPCIÓN DEL PROBLEMA', '', 2, '2023-02-28 22:23:56.618', 9, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(12, 'PROPÓSITO DEL PROYECTO', '', 3, '2023-02-28 22:24:21.390', 9, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(13, 'ESTADO DEL ARTE', '', 4, '2023-02-28 22:24:44.501', 9, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(14, 'SOLUCIÓN PLANTEADA', '', 5, '2023-02-28 22:25:12.962', 9, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(15, 'ALCANCES Y RESTRICCIONES', '', 6, '2023-02-28 22:25:38.526', 9, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(16, 'PLANTEAMIENTOS DE OBJETIVOS', '', 3, '2023-02-28 22:26:02.754', NULL, 2, 1, NULL, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(17, 'GENERAL', '', 1, '2023-02-28 22:26:21.583', 15, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(18, 'ESPECÍFICOS', '', 2, '2023-02-28 22:26:45.269', 15, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(19, 'ESTUDIO DE FACTIBILIDAD Y GESTIÓN DE RIESGOS', '', 4, '2023-02-28 22:27:30.306', NULL, 2, 1, NULL, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(20, 'ESTUDIO DE FACTIBILIDAD', '', 1, '2023-02-28 22:28:06.647', 18, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(21, 'FACTIBILIDAD TÉCNICA', '', 1, '2023-02-28 22:28:35.274', 19, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(22, 'ANÁLISIS COSTO BENEFICIO A UN AÑO', '', 2, '2023-02-28 22:29:19.778', 19, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(23, 'FACTIBILIDAD OPERACIONAL', '', 3, '2023-02-28 22:29:50.007', 19, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(24, 'FACTIBILIDAD LEGAL', '', 4, '2023-02-28 22:30:15.036', 19, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(25, 'IDENTIFCACIÓN DE RIESGOS', '', 2, '2023-02-28 22:30:48.106', 18, 2, 1, NULL, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(26, 'RIESGOS DE PLANEACIÓN', '', 1, '2023-02-28 22:31:14.897', 24, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(27, 'RIESGOS DE DESARROLLO', '', 2, '2023-02-28 22:31:46.313', 24, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(28, 'RIESGOS DEL CLIENTE', '', 3, '2023-02-28 22:32:06.483', 24, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(29, 'RIESGOS DE IMPLEMENTACIÓN', '', 4, '2023-02-28 22:32:38.428', 24, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(30, 'PLANTEAMIENTO DE LA SOLUCIÓN', '', 5, '2023-02-28 22:33:13.797', NULL, 2, 1, NULL, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(31, 'ANÁLISIS DE LA SOLUCIÓN', '', 1, '2023-02-28 22:33:41.795', 29, 2, 1, NULL, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(32, 'DESCRIPCIÓN DE LA SOLUCIÓN PROPUESTA EN DETALLE', '', 1, '2023-02-28 22:34:18.568', 30, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(33, 'EVALUACIÓN DE HERRRAMIENTAS DE DESARROLLO E IMPLEMENTACIÓN', '', 2, '2023-02-28 22:34:56.603', 30, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(34, 'DIAGRAMA DE ARQUITECTURA DE SOLUCIÓN PROPUESTA EN DETALLE', '', 3, '2023-02-28 22:35:41.260', 30, 2, 1, 2, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(35, 'DIAGRAMA PROCESO MEJORADO (BPMN)', '', 4, '2023-02-28 22:36:13.624', 30, 2, 1, 2, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(36, 'METODOLOGÍA APLICADA', '', 2, '2023-02-28 22:36:35.291', 29, 2, 1, NULL, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(37, 'COMPARATIVA DE METODOLOGÍAS ASOCIADAS AL PROYECTO', '', 1, '2023-02-28 22:37:22.909', 35, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(38, 'JUSTIFICACIÓN DE LA METODOLOGÍA SELECCIONADA', '', 2, '2023-02-28 22:38:05.780', 35, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(39, 'METODOLOGÍA DE ADMINISTRACIÓN', '', 3, '2023-02-28 22:38:31.960', 35, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(40, 'CARTA GANTT', '', 4, '2023-02-28 22:38:59.153', 35, 2, 1, 2, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(41, 'OBTENCIÓN DE REQUERIMIENTOS', '', 3, '2023-02-28 22:39:36.957', 29, 2, 1, NULL, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(42, 'METODOLOGÍA APLICADA A LA TOMA DE REQUERIMIENTOS', '', 1, '2023-02-28 22:40:22.286', 40, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(43, 'REQUERIMIENTOS FUNCIONALES', '', 2, '2023-02-28 22:40:46.597', 40, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(44, 'REQUERIMIENTOS NO FUNCIONALES', '', 3, '2023-02-28 22:41:22.361', 40, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(45, 'REQUERIMIENTOS DE SEGURIDAD', '', 4, '2023-02-28 22:41:51.002', 40, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(46, 'REQUERIMIENTOS DE MANTENCIÓN', '', 5, '2023-02-28 22:42:20.300', 40, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(47, 'ESPECIFICACIÓN DE REQUERIMIENTO', '', 6, '2023-02-28 22:42:59.092', 40, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(48, 'DISEÑO DEL SISTEMA', '', 6, '2023-02-28 22:43:19.725', NULL, 2, 1, NULL, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(49, 'MODELAMIENTO UML', '', 1, '2023-02-28 22:43:49.186', 47, 2, 1, NULL, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(50, 'DIAGRAMA CASOS DE USOS (DEBE SER INCLUSIÓN O EXTENSIÓN)', '', 1, '2023-02-28 22:44:47.063', 48, 2, 1, 2, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(51, 'DOCUMENTACIÓN CASOS DE USO', '', 2, '2023-02-28 22:45:26.241', 48, 2, 1, 2, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(52, 'DIAGRAMA DE COMPONENTES', '', 3, '2023-02-28 22:45:51.424', 48, 2, 1, 2, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(53, 'CONSTRUCCIÓN DE PROTOTIPO FUNCIONAL', '', 7, '2023-02-28 22:49:27.219', NULL, 2, 1, 2, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(54, 'MODELO ENTIDAD RELACIÓN O MODELO DE DATOS DEPENDE DEL PROYECTO', '', 2, '2023-02-28 22:50:18.882', 47, 2, 1, 2, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(55, 'DISEÑOS DE PRUEBAS DEL SOFTWARE', '', 8, '2023-02-28 22:51:26.315', NULL, 2, 1, 2, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(56, 'CONCLUSIONES DEL PROYECTO', '', 9, '2023-02-28 22:51:51.215', NULL, 2, 1, NULL, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(57, 'CONCLUSIONES', '', 1, '2023-02-28 22:52:32.663', 55, 2, 1, 1, false);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, responsable_id, seccion_id, tipo_entrada_id, ind_base)
            VALUES(58, 'PERSPECTIVAS FUTURAS', '', 2, '2023-02-28 22:53:03.082', 55, 2, 1, 1, false);
            SELECT setval('actividad_id_seq',59, true);
            --se crea vista para asociar respuestas a preguntas
            create or replace VIEW proyectoseccion as 
            select 
            t1.id as proyecto_id,t2.seccion_id, (
                select to_json(array_agg(row_to_json(actividades))) from (
                    select s1.orden,s1.id,s1.nombre,s1.descripcion,s1.actividad_padre_id,s1.seccion_id,s1.tipo_entrada_id,s1.ind_base,
                        case when (select count(*) from actividad p3 where p3.actividad_padre_id= s1.id) > 0 
                        then (
                            select to_json(array_agg(row_to_json(actividades_hijas))) from (
                                select p1.orden,p1.id,p1.nombre,p1.descripcion,p1.actividad_padre_id,p1.seccion_id,p1.tipo_entrada_id,p1.ind_base,
                                    case when (select count(*) from actividad o3 where o3.actividad_padre_id= p1.id) > 0 
                                    then (
                                        select to_json(array_agg(row_to_json(actividades_nietas))) from (
                                            select o1.orden,o1.id,o1.nombre,o1.descripcion,o1.actividad_padre_id,o1.seccion_id,o1.tipo_entrada_id,o1.ind_base
                                            from actividad o1 where o1.actividad_padre_id= p1.id order by o1.orden
                                        ) actividades_nietas
                                    ) else null end as actividades_nietas,
                                    case when (select count(*) from actividad_respuesta_proyecto o4 where o4.proyecto_id = t1.id and o4.actividad_id = p1.id)>0
                                    then (
                                        select to_json(array_agg(row_to_json(respuestas))) from (
                                            select o2.respuesta,o2.ind_publicada,o2.fecha from actividad_respuesta_proyecto o2 where o2.proyecto_id = t1.id and o2.actividad_id = p1.id
                                        ) respuestas
                                    ) else null end as respuestas
                                from actividad p1 where p1.actividad_padre_id= s1.id order by p1.orden
                            ) actividades_hijas
                        ) else null end as actividades_hijas,
                        case when (select count(*) from actividad_respuesta_proyecto p4 where p4.proyecto_id = t1.id and p4.actividad_id = s1.id)>0
                        then (
                            select to_json(array_agg(row_to_json(respuestas))) from (
                                select p2.respuesta,p2.ind_publicada,p2.fecha from actividad_respuesta_proyecto p2 where p2.proyecto_id = t1.id and p2.actividad_id = s1.id
                            ) respuestas
                        ) else null end as respuestas
                    from actividad s1
                    where s1.seccion_id = 1 and s1.actividad_padre_id is null
                    order by s1.orden
                ) actividades
            ) as actividades 
            from proyecto t1
            inner join alumno_seccion t2 on t1.alumno_seccion_id = t2.id;
            """).execute_lines()
        except Exception as exc:
            logging.warning(formatear_error(exc))
            print(formatear_error(exc))