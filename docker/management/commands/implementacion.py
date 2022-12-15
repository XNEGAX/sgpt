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
            --USUARIO DEMO
            INSERT INTO public.auth_user (id, "password", last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
            VALUES(1, '', now(), false, '173733321@ACADEMICOS.uamericas.cl', 'CARLOS', 'MARIN GONZALEZ', 'carlos.marin.gonzalez@edu.udla.cl', true, true, now());
            SELECT setval('auth_user_id_seq',2, true);
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
            VALUES(1, 'Inicio', 'home:home', 'tf-icons bx bx-home-circle', 0, now(), NULL, 0, 1);
            INSERT INTO public.modulo(id, nombre, url, icono, orden, fecha, modulo_padre_id, responsable_id, tipo_modulo_id)
            VALUES(2, 'Cambio Perfil', 'guard:cambio_perfil', 'tf-icons bx bx-home-circle', 0, now(), NULL, 0, 2);
            INSERT INTO public.modulo(id, nombre, url, icono, orden, fecha, modulo_padre_id, responsable_id, tipo_modulo_id)
            VALUES(3, 'MANTENEDORES', '', '', 2, now(), NULL, 0, 1);
            INSERT INTO public.modulo(id, nombre, url, icono, orden, fecha, modulo_padre_id, responsable_id, tipo_modulo_id)
            VALUES(4, 'USUARIO', 'guard:mantenedor_usuario', 'tf-icons bx bx-user-plus', 2, now(), 3, 0, 1);
            SELECT setval('modulo_id_seq',5, true);
            --PERFIL
            INSERT INTO public.perfil(id,nombre, fecha, responsable_id)VALUES(1,'ADMINISTRADOR',now(),0);
            INSERT INTO public.perfil(id,nombre, fecha, responsable_id)VALUES(2,'PROFESOR',now(),0);
            INSERT INTO public.perfil(id,nombre, fecha, responsable_id)VALUES(3,'ALUMNO',now(),0);
            INSERT INTO public.perfil(id,nombre, fecha, responsable_id)VALUES(4,'INVITADO',now(),0);
            SELECT setval('perfil_id_seq',5, true);
            --PARAMETRO PERFIL INVITADO
            INSERT INTO public.parametro(nombre,metadatos, fecha, responsable_id)VALUES('perfil_invitado',cast('{"perfil_id": "4"}' AS json),now(),0);
            --PERFIL ACTIVO USUARIO DEMO
            INSERT INTO public.usuario_perfil_activo(fecha, perfil_id, responsable_id, usuario_id)VALUES(now(),1, 0, 1);
            --PERMISOS USUARIO DEMO
            INSERT INTO public.usuario_perfil_modulo(modulo_id,perfil_id,usuario_id,permiso,fecha,responsable_id)VALUES(1,1,1,'["GET"]',NOW(),0);
            INSERT INTO public.usuario_perfil_modulo(modulo_id,perfil_id,usuario_id,permiso,fecha,responsable_id)VALUES(2,1,1,'["GET","PUT"]',NOW(),0);
            INSERT INTO public.usuario_perfil_modulo(modulo_id,perfil_id,usuario_id,permiso,fecha,responsable_id)VALUES(3,1,1,'["GET"]',NOW(),0);
            INSERT INTO public.usuario_perfil_modulo(modulo_id,perfil_id,usuario_id,permiso,fecha,responsable_id)VALUES(4,1,1,'["GET","POST","PUT","DELETE"]',NOW(),0);
            INSERT INTO public.usuario_perfil_modulo(modulo_id,perfil_id,usuario_id,permiso,fecha,responsable_id)VALUES(1,2,1,'["GET"]',NOW(),0);
            INSERT INTO public.usuario_perfil_modulo(modulo_id,perfil_id,usuario_id,permiso,fecha,responsable_id)VALUES(2,2,1,'["GET","PUT"]',NOW(),0);
            INSERT INTO public.usuario_perfil_modulo(modulo_id,perfil_id,usuario_id,permiso,fecha,responsable_id)VALUES(1,3,1,'["GET"]',NOW(),0);
            INSERT INTO public.usuario_perfil_modulo(modulo_id,perfil_id,usuario_id,permiso,fecha,responsable_id)VALUES(2,3,1,'["GET","PUT"]',NOW(),0);
            INSERT INTO public.usuario_perfil_modulo(modulo_id,perfil_id,usuario_id,permiso,fecha,responsable_id)VALUES(1,4,1,'["GET"]',NOW(),0);
            --ACCESO INVITADO
            INSERT INTO public.parametro(nombre,metadatos, fecha, responsable_id)VALUES('acceso_invitado','{"modulo_id": "1","perfil_id":"4","permiso":["GET"]}'::jsonb,now(),0);
            -- SP PERMISOS MODULO USUARIO
            CREATE OR REPLACE FUNCTION public.sp_web_get_permisos_modulo_usuario(p_usuario_id int4)
            RETURNS TABLE(perfil_activo text,cantidad_perfiles int4,modulos json)
            LANGUAGE plpgsql
            AS $function$BEGIN
            RETURN QUERY 	 
            select T2.nombre as perfil_activo, (
                select count(distinct p1.perfil_id) from public.usuario_perfil_modulo  p1
                where p1.usuario_id = t1.usuario_id and p1.perfil_id::int4 != (
                    SELECT (pa1.metadatos::jsonb->>'perfil_id')::int4 FROM public.parametro pa1 WHERE pa1.nombre='perfil_invitado' limit 1
                )::int4
            )::int4 as cantidad_perfiles,(
                select to_json(array_agg(row_to_json(listado_modulos))) from (
                    select initcap(m2.nombre) as nombre, m2.url,m2.icono,m3.nombre as tipo,to_jsonb(m1.permiso) as permisos, m2.orden,(
                        select to_json(array_agg(row_to_json(listado_submodulos))) from (
                            select initcap(s2.nombre) as nombre, s2.url,s2.icono,s3.nombre as tipo,to_jsonb(s1.permiso) as permisos, s2.orden
                            from public.usuario_perfil_modulo s1
                            inner join public.modulo s2 on s1.modulo_id = s2.id
                            inner join public.tipo_modulo s3 on s2.tipo_modulo_id = s3.id
                            where s1.usuario_id = t1.usuario_id and s1.perfil_id = t2.id and s2.modulo_padre_id = m1.modulo_id
                            order by s2.orden 
                        ) listado_submodulos
                    ) as submodulos
                    from public.usuario_perfil_modulo m1
                    inner join public.modulo m2 on m1.modulo_id = m2.id
                    inner join public.tipo_modulo m3 on m2.tipo_modulo_id = m3.id
                    where m1.usuario_id = t1.usuario_id and m1.perfil_id = t2.id and m2.modulo_padre_id is null
                    order by m2.orden
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
            print(formatear_error(exc))