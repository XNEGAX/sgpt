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
            SELECT setval('auth_user_id_seq',1, true);
            --PARAMETROS BASE PARA TIPO MODULO
            INSERT INTO public.parametro(nombre,metadatos, fecha, responsable_id)VALUES('auth_user_auto',cast('{"auth_user_id": "0"}' AS json),now(),0);
            --TIPOS DE MODULOS
            INSERT INTO public.tipo_modulo(id,nombre, fecha, responsable_id)VALUES(1,'MENU',now(),0);
            INSERT INTO public.tipo_modulo(id,nombre, fecha, responsable_id)VALUES(2,'API',now(), 0);
            INSERT INTO public.tipo_modulo(id,nombre, fecha, responsable_id)VALUES(3,'BOTÓN',now(), 0);
            INSERT INTO public.tipo_modulo(id,nombre, fecha, responsable_id)VALUES(4,'BANNER',now(), 0);
            SELECT setval('tipo_modulo_id_seq',5, true);
            --PARAMETROS BASE PARA TIPO MODULO
            INSERT INTO public.parametro(nombre,metadatos, fecha, responsable_id)VALUES('tipo_modulo_menu',cast('{"tipo_modulo_id": "1"}' AS json),now(),0);
            INSERT INTO public.parametro(nombre,metadatos, fecha, responsable_id)VALUES('tipo_modulo_api',cast('{"tipo_modulo_id": "2"}' AS json),now(),0);
            INSERT INTO public.parametro(nombre,metadatos, fecha, responsable_id)VALUES('tipo_modulo_boton',cast('{"tipo_modulo_id": "3"}' AS json),now(),0);
            INSERT INTO public.parametro(nombre,metadatos, fecha, responsable_id)VALUES('tipo_modulo_banner',cast('{"tipo_modulo_id": "4"}' AS json),now(),0);
            --MODULOS
            INSERT INTO public.modulo(id, nombre, url, icono, orden, fecha, modulo_padre_id, responsable_id, tipo_modulo_id)
            VALUES(1, 'HOME', 'home:home', 'tf-icons bx bx-home-circle', 0, '2022-12-07 09:16:27.498', NULL, 0, 1);
            INSERT INTO public.modulo(id, nombre, url, icono, orden, fecha, modulo_padre_id, responsable_id, tipo_modulo_id)
            VALUES(2, 'MANTENEDORES', '', '', 2, '2022-12-07 19:13:24.697', NULL, 0, 1);
            INSERT INTO public.modulo(id, nombre, url, icono, orden, fecha, modulo_padre_id, responsable_id, tipo_modulo_id)
            VALUES(3, 'USUARIOS', 'guard:usuarios', '', 1, '2022-12-07 19:13:24.736', 2, 0, 1);
            INSERT INTO public.modulo(id, nombre, url, icono, orden, fecha, modulo_padre_id, responsable_id, tipo_modulo_id)
            VALUES(4, 'SECCIONES', 'guard:seccion', '', 2, '2022-12-07 19:13:24.736', 2, 0, 1);
            SELECT setval('modulo_id_seq',5, true);
            --ROLES
            INSERT INTO public.rol(id, nombre, fecha, responsable_id)VALUES(1, 'GENERICO', NOW(), 0);
            INSERT INTO public.rol(id, nombre, fecha, responsable_id)VALUES(2, 'MANTENEDORES', NOW(), 0);
            INSERT INTO public.rol(id, nombre, fecha, responsable_id)VALUES(3, 'MANTENEDOR DE USUARIOS', NOW(), 0);
            INSERT INTO public.rol(id, nombre, fecha, responsable_id)VALUES(4, 'MANTENEDOR DE SECCIONES', NOW(), 0);
            INSERT INTO public.rol(id, nombre, fecha, responsable_id)VALUES(5, 'MANTENEDOR DE ACTIVIDADES', NOW(), 0);
            INSERT INTO public.rol(id, nombre, fecha, responsable_id)VALUES(6, 'MANTENEDOR DE FASES', NOW(), 0);
            INSERT INTO public.rol(id, nombre, fecha, responsable_id)VALUES(7, 'MANTENEDOR DE PROYECTOS', NOW(), 0);
            SELECT setval('rol_id_seq',8, true);
            --PERFIL
            INSERT INTO public.perfil(id,nombre, editable, fecha, responsable_id)VALUES(1,'ADMINISTRADOR', false,now(),0);
            INSERT INTO public.perfil(id,nombre, editable, fecha, responsable_id)VALUES(2,'DOCENTE', false,now(),0);
            INSERT INTO public.perfil(id,nombre, editable, fecha, responsable_id)VALUES(3,'ESTUDIANTE', false,now(),0);
            INSERT INTO public.perfil(id,nombre, editable, fecha, responsable_id)VALUES(4,'INVITADO', false,now(),0);
            SELECT setval('perfil_id_seq',8, true);
            --PARAMETRO PERFIL INVITADO
            INSERT INTO public.parametro(nombre,metadatos, fecha, responsable_id)VALUES('perfil_invitado',cast('{"perfil_id": "4"}' AS json),now(),0);
            --RELACION PERFIL ROL
            INSERT INTO public.perfil_rol(id, fecha, perfil_id, responsable_id, rol_id)VALUES(1, NOW(), 1, 0, 1);
            INSERT INTO public.perfil_rol(id, fecha, perfil_id, responsable_id, rol_id)VALUES(2, NOW(), 1, 0, 2);
            INSERT INTO public.perfil_rol(id, fecha, perfil_id, responsable_id, rol_id)VALUES(3, NOW(), 1, 0, 3);
            INSERT INTO public.perfil_rol(id, fecha, perfil_id, responsable_id, rol_id)VALUES(4, NOW(), 1, 0, 4);
            INSERT INTO public.perfil_rol(id, fecha, perfil_id, responsable_id, rol_id)VALUES(5, NOW(), 4, 0, 1);
            SELECT setval('perfil_rol_id_seq',6, true);
            --PARAMETRO PERFIL ROL GENERICO-INVITADO
            INSERT INTO public.parametro(nombre,metadatos, fecha, responsable_id)VALUES('perfil_rol_generico_invitado',cast('{"perfil_rol_id": "5"}' AS json),now(),0);
            --RELACION MODULO ROL
            INSERT INTO public.modulo_rol(id, fecha, modulo_id, responsable_id, rol_id)VALUES(1,NOW(), 1, 0, 1);
            INSERT INTO public.modulo_rol(id, fecha, modulo_id, responsable_id, rol_id)VALUES(2,NOW(), 2, 0, 2);
            INSERT INTO public.modulo_rol(id, fecha, modulo_id, responsable_id, rol_id)VALUES(3,NOW(), 3, 0, 3);
            INSERT INTO public.modulo_rol(id, fecha, modulo_id, responsable_id, rol_id)VALUES(4,NOW(), 4, 0, 4);
            SELECT setval('modulo_rol_id_seq',5, true);
            -- SP PERMISOS MODULO USUARIO
            CREATE OR REPLACE FUNCTION public.sp_web_get_permisos_modulo_usuario(p_usuario_id int4)
            RETURNS TABLE(perfil_activo text,cantidad_perfiles int4,modulos json)
            LANGUAGE plpgsql
            AS $function$BEGIN
            RETURN QUERY 	 
            select T2.nombre as perfil_activo, (
            select count(distinct p2.perfil_id) from public.usuario_perfil_rol p1
            inner join public.perfil_rol p2 on p1.perfil_rol_id = p2.id
            where p1.usuario_id = t1.usuario_id and p2.perfil_id::int4 != (
                SELECT pa1.metadatos->>perfil_id::int4 FROM public.parametro pa1 WHERE pa1.nombre='perfil_invitado' limit 1)::int4
                )::int4 as cantidad_perfiles,(
                    select to_json(array_agg(row_to_json(listado_modulos))) from (
                        select initcap(m4.nombre) as nombre, m4.url,m4.icono,m5.nombre as tipo,m1.permiso::json as permisos,(
                            select to_json(array_agg(row_to_json(listado_submodulos))) from (
                                select initcap(s4.nombre) as nombre, s4.url,s4.icono,s5.nombre as tipo,s1.permiso::json as permisos
                                from usuario_perfil_rol s1
                                inner join perfil_rol s2 on s1.perfil_rol_id = s2.id
                                inner join modulo_rol s3 on s2.rol_id = s3.rol_id
                                inner join modulo s4 on s3.modulo_id = s4.id
                                inner join tipo_modulo s5 on s4.tipo_modulo_id = s5.id
                                where s1.usuario_id = t1.usuario_id and s2.perfil_id = t1.perfil_id and s4.modulo_padre_id = m4.id
                                order by s4.orden
                            ) listado_submodulos
                        ) as submodulos
                        from usuario_perfil_rol m1
                        inner join perfil_rol m2 on m1.perfil_rol_id = m2.id
                        inner join modulo_rol m3 on m2.rol_id = m3.rol_id
                        inner join modulo m4 on m3.modulo_id = m4.id
                        inner join tipo_modulo m5 on m4.tipo_modulo_id = m5.id
                        where m1.usuario_id = t1.usuario_id and m2.perfil_id = t1.perfil_id and m4.modulo_padre_id is null
                        order by m4.orden
                    ) listado_modulos
                ) as modulos
                from public.usuario_perfil_activo t1
                inner join public.perfil t2 on t1.perfil_id = t2.id
                where t1.usuario_id = p_usuario_id;
            END;$function$
            ;
            """).execute_lines()
        except Exception as exc:
            logging.warning(formatear_error(exc))