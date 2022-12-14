# Generated by Django 3.2.6 on 2022-12-14 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('nombre', models.TextField()),
                ('descripcion', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_actividad', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'actividad',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='EstadoCivil',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=10, unique=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_estado_civil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'estado_civil',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Fase',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('nombre', models.TextField()),
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
            name='Nacionalidad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.TextField(unique=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_nacionalidad', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'nacionalidad',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre', models.TextField(unique=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_perfil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'perfil',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UsuarioPerfilActivo',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('perfil', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='usuarioperfilactivo_set', to='guard.perfil')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_usuario_perfil_actibo', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'usuario_perfil_activo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoSalidaReporte',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('nombre', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_tipo_salida_reporte', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tipo_salida_reporte',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoModulo',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre', models.TextField(unique=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_tipo_modulo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tipo_modulo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoEntrada',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('tipo', models.TextField()),
                ('ind_archivo', models.BooleanField(default=True)),
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
            name='Sexo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=9, unique=True)),
                ('acronimo', models.CharField(max_length=1, unique=True, verbose_name='Acrónimo')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_sexo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'sexo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('codigo', models.TextField()),
                ('nombre', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_seccion', to=settings.AUTH_USER_MODEL)),
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
                ('tipo_salida_reporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guard.tiposalidareporte')),
            ],
            options={
                'db_table': 'reporte_configurable',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('fecha_nacimiento', models.DateField()),
                ('telefono', models.BigIntegerField(blank=True, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('estado_civil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persona_estado_civil', to='guard.estadocivil')),
                ('nacionalidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='guard.nacionalidad')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_persona', to=settings.AUTH_USER_MODEL)),
                ('sexo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guard.sexo')),
                ('usuario', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'persona',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Parametro',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('nombre', models.TextField(unique=True)),
                ('metadatos', models.JSONField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_parametro', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'parametro',
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
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('modulo_padre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relacion_modulo_padre', to='guard.modulo')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_modulo', to=settings.AUTH_USER_MODEL)),
                ('tipo_modulo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='guard.tipomodulo')),
            ],
            options={
                'db_table': 'modulo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FaseActividadTipoEntrada',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('orden', models.IntegerField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guard.actividad')),
                ('fase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guard.fase')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_face_actividad_tipo_entrada', to=settings.AUTH_USER_MODEL)),
                ('tipo_entrada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guard.tipoentrada')),
            ],
            options={
                'db_table': 'fase_actividad_tipo_entrada',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FaseActividadRespuestaUsuario',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('respuesta', models.TextField()),
                ('ind_publicada', models.BooleanField(default=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('fase_actividad_tipo_entrada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guard.faseactividadtipoentrada')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_face_actividad_respuesta_usuario', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'fase_actividad_respuesta_persona',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FaseActividadRespuestaEntrada',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('respuesta', models.TextField()),
                ('orden', models.IntegerField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('fase_actividad_tipo_entrada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guard.faseactividadtipoentrada')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_face_actividad_respuesta_entrada', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'fase_actividad_respuesta_entrada',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='fase',
            name='seccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guard.seccion'),
        ),
        migrations.CreateModel(
            name='ConfiguracionBase',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('metadatos', models.JSONField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('modelo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_configuracionbase', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'configuracion_base',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BitacoraFaseActividadRespuestaUsuario',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('comentario', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('bitacora_padre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='guard.bitacorafaseactividadrespuestausuario')),
                ('fase_actividad_respuesta_persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guard.faseactividadrespuestausuario')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_bitacora_face_actividad_respuesta_usuario', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bitacora_fase_actividad_respuesta_persona',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UsuarioPerfilModulo',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('permiso', models.JSONField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuarioperfilmodulo_modulo_set', to='guard.modulo')),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuarioperfilmodulo_perfil_set', to='guard.perfil')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_crud_usuario_perfil_modulo', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuarioperfilmodulo_modulo_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'usuario_perfil_modulo',
                'managed': True,
                'unique_together': {('perfil_id', 'modulo_id', 'usuario_id')},
            },
        ),
    ]
