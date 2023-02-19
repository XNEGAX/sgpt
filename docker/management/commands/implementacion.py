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
            VALUES(8,'sección', 'proyecto:mantenedor_secciones', 'tf-icons bx bxs-factory',2, true, 3);
            INSERT INTO public.modulo(id,nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(7,'Fase', 'proyecto:mantenedor_fases', 'tf-icons bx bxs-factory',1, true, 3);
            INSERT INTO public.modulo(id, nombre, url, icono, orden, ind_url, modulo_padre_id)
            VALUES(10, 'Administrar proyecto título', 'proyecto:mantenedor_proyecto', 'tf-icons bx bxs-factory', 5, true, null);
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
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(9,3,2);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(10,4,1);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(11,5,1);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(13,7,2);
            INSERT INTO public.perfil_modulo(id,modulo_id, perfil_id)VALUES(14,8,1);
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
            --FASES
            INSERT INTO public.fase(id, nombre, descripcion, fecha, responsable_id)VALUES(1, 'ASPECTOS DE LA EMPRESA', '', now(), 1);
            INSERT INTO public.fase(id, nombre, descripcion, fecha, responsable_id)VALUES(2, 'SITUACIÓN ACTUAL DEL PROYECTO', '', now(), 1);
            INSERT INTO public.fase(id, nombre, descripcion, fecha, responsable_id)VALUES(3, 'PLANTEAMIENTO DE OBJETIVOS', '', now(), 1);
            INSERT INTO public.fase(id, nombre, descripcion, fecha, responsable_id)VALUES(4, 'ESTUDIO DE FACTIBILIDAD Y GESTIÓN DE RIESGOS', '', 'now()', 1);
            INSERT INTO public.fase(id, nombre, descripcion, fecha, responsable_id)VALUES(5, 'PLANTEAMIENTO DE LA SOLUCION', '', now(), 1);
            INSERT INTO public.fase(id, nombre, descripcion, fecha, responsable_id)VALUES(6, 'DISEÑO DEL SISTEMA', '', now(), 1);
            INSERT INTO public.fase(id, nombre, descripcion, fecha, responsable_id)VALUES(7, 'CONSTRUCCIÓN DE PROTOTIPO FUNCIONAL ', '', now(), 1);
            INSERT INTO public.fase(id, nombre, descripcion, fecha, responsable_id)VALUES(8, 'DISEÑOS DE PRUEBAS DEL SOFTWARE', '', now(), 1);
            INSERT INTO public.fase(id, nombre, descripcion, fecha, responsable_id)VALUES(9, 'CONCLUSIONES DEL PROYECTO', '', now(), 1);
            SELECT setval('fase_id_seq',10, true);
            --tipos dato
            INSERT INTO public.tipo_entrada(id, nombre, tipo, ind_archivo, ind_multiple, formato, fecha, responsable_id)VALUES(1, 'TEXTO','text', false, false, NULL, now(), 0);
            INSERT INTO public.tipo_entrada(id, nombre, tipo, ind_archivo, ind_multiple, formato, fecha, responsable_id)VALUES(2, 'IMAGEN','file', false, false,'jpeg', now(), 0);
            SELECT setval('tipo_entrada_id_seq',3, true);
            --actividades
            INSERT INTO public.actividad(id, actividad_padre_id, nombre, descripcion, orden, fecha, fase_id, responsable_id, seccion_id, tipo_entrada_id)
            VALUES(1, null ,'INTRODUCCIÓN', 'ESTE CAPÍTULO CONSISTE EN UNA EXPOSICIÓN BREVE DEL PROBLEMA QUE SE PRETENDE SOLUCIONAR Y/O INVESTIGAR. TODA INFORMACIÓN DEBERÁ IR ACOMPAÑADA DE LA CORRESPONDIENTE CITA BIBLIOGRÁFICA, COMO SE INDICA MÁS ADELANTE. LA INTRODUCCIÓN TAMBIÉN DEBE PRESENTAR LA RELEVANCIA DEL PROYECTO O INVESTIGACIÓN.',
            1, now(), NULL, 2, 1, 1);
            INSERT INTO public.actividad(id, actividad_padre_id, nombre, descripcion, orden, fecha, fase_id, responsable_id, seccion_id, tipo_entrada_id)
            VALUES(2, null, 'ANTECEDENTES DE LA EMPRESA.', '-', 
            2, now(), 1, 2, 1, 1);
            INSERT INTO public.actividad(id, actividad_padre_id, nombre, descripcion, orden, fecha, fase_id, responsable_id, seccion_id, tipo_entrada_id)
            VALUES(3, null, 'ORGANIGRAMA', '-', 
            3, now(), 1, 2, 1, 2);
            INSERT INTO public.actividad(id, nombre, descripcion, orden, fecha, actividad_padre_id, fase_id, responsable_id, seccion_id, tipo_entrada_id)VALUES(5, 'ÁREA FUNCIONAL', '-', 
            4, now(), NULL, 1, 2, 1, 1);
            SELECT setval('actividad_id_seq',5, true);

            """).execute_lines()
        except Exception as exc:
            logging.warning(formatear_error(exc))
            print(formatear_error(exc))