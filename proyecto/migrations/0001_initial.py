# Generated by Django 3.2.6 on 2023-02-14 02:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('nombre', models.TextField()),
                ('descripcion', models.TextField(default='-')),
                ('orden', models.FloatField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('actividad_padre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relacion_actividad_padre', to='proyecto.actividad')),
            ],
            options={
                'db_table': 'actividad',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ActividadRespuestaUsuario',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('respuesta', models.TextField()),
                ('ind_publicada', models.BooleanField(default=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relacion_actividad_respuesta_usuario', to='proyecto.actividad')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_actividad_respuesta_usuario', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'actividad_respuesta_usuario',
                'managed': True,
                'unique_together': {('actividad', 'usuario', 'respuesta')},
            },
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('folio', models.TextField()),
                ('nombre', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_documento', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'documento',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre', models.TextField()),
                ('url', models.TextField()),
                ('icono', models.TextField(blank=True, null=True)),
                ('orden', models.IntegerField()),
                ('ind_url', models.BooleanField(default=True)),
                ('modulo_padre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relacion_modulo_padre', to='proyecto.modulo')),
            ],
            options={
                'db_table': 'modulo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Parametro',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('nombre', models.TextField(unique=True)),
                ('metadatos', models.JSONField()),
            ],
            options={
                'db_table': 'parametro',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre', models.TextField(unique=True)),
                ('ind_asignable', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'perfil',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Semestre',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'semestre',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='VersionDocumento',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('version', models.IntegerField()),
                ('metadatos', models.JSONField()),
                ('ruta', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.documento')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_version_documento', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'version_documento',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoEntrada',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('nombre', models.TextField()),
                ('tipo', models.TextField()),
                ('ind_archivo', models.BooleanField(default=False)),
                ('ind_multiple', models.BooleanField(default=False)),
                ('formato', models.TextField(blank=True, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_tipo_entrada', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tipo_entrada',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.TextField()),
                ('mnemonico', models.CharField(max_length=10)),
                ('folio_correlativo', models.IntegerField()),
                ('ruta', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_tipo_documento', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tipo_documento',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('codigo', models.TextField(unique=True)),
                ('fecha_desde', models.DateTimeField()),
                ('fecha_hasta', models.DateTimeField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_seccion', to=settings.AUTH_USER_MODEL)),
                ('semestre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seccion_semestre', to='proyecto.semestre')),
            ],
            options={
                'db_table': 'seccion',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ReporteConfigurable',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('nombre', models.TextField()),
                ('codigo_fuente', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_reporte_configurable', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'reporte_configurable',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('accion', models.IntegerField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('metadatos', models.JSONField()),
                ('modelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='autor_log', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'log',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Fase',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('nombre', models.TextField(unique=True)),
                ('descripcion', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_fase', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'fase',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='EstadoDocumento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_estado_documento', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'estado_documento',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='documento',
            name='tipo_documento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.tipodocumento'),
        ),
        migrations.CreateModel(
            name='BitacoraActividadRespuestaUsuario',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('comentario', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('actividad_respuesta_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.actividadrespuestausuario')),
                ('bitacora_padre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.bitacoraactividadrespuestausuario')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_bitacora_actividad_respuesta_usuario', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bitacora_actividad_respuesta_usuario',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='actividad',
            name='fase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.fase'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='responsable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_actividad', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='actividad',
            name='seccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.seccion'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='tipo_entrada',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.tipoentrada'),
        ),
        migrations.CreateModel(
            name='PerfilUsuarioActivo',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_perfil_activo_perfil', to='proyecto.perfil')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_usuario_perfil_actibo', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'usuario_perfil_activo',
                'managed': True,
                'unique_together': {('perfil_id', 'usuario_id')},
            },
        ),
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_usuario_perfil', to='proyecto.perfil')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_perfil_usuario', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_usuario_usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'perfil_usuario',
                'managed': True,
                'unique_together': {('perfil_id', 'usuario_id')},
            },
        ),
        migrations.CreateModel(
            name='PerfilModulo',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_modulo_modulo', to='proyecto.modulo')),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_modulo_perfil', to='proyecto.perfil')),
            ],
            options={
                'db_table': 'perfil_modulo',
                'managed': True,
                'unique_together': {('perfil_id', 'modulo_id')},
            },
        ),
        migrations.CreateModel(
            name='DocenteSeccion',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_docente_seccion', to=settings.AUTH_USER_MODEL)),
                ('seccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.seccion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'docente_seccion',
                'managed': True,
                'unique_together': {('usuario', 'seccion')},
            },
        ),
        migrations.CreateModel(
            name='AlumnoSeccion',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_alumno_seccion', to=settings.AUTH_USER_MODEL)),
                ('seccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.seccion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'alumno_seccion',
                'managed': True,
                'unique_together': {('usuario', 'seccion')},
            },
        ),
    ]
