from proyecto.log import LogManager
import json
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
 
class Modulo(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField(blank=False, null=False)
    url = models.TextField(blank=False, null=False)
    modulo_padre = models.ForeignKey('self',on_delete=models.CASCADE, related_name='fk_relacion_modulo_padre',blank=True, null=True,db_column='modulo_padre_id')
    icono = models.TextField(blank=True, null=True)
    orden = models.IntegerField(blank=False, null=False)
    ind_url = models.BooleanField(default=True)
    
    class Meta:
        managed = True
        db_table = 'modulo'

class Perfil(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField(blank=False, null=False, unique=True)
    ind_asignable = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'perfil'

    def __str__(self):
        return self.nombre

class PerfilModulo(models.Model):
    id = models.BigAutoField(primary_key=True)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE,related_name='fk_perfil_modulo_perfil',db_column='perfil_id')
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE,related_name='fk_perfil_modulo_modulo',db_column='modulo_id')

    class Meta:
        managed = True
        db_table = 'perfil_modulo'
        unique_together = ('perfil_id', 'modulo_id',)

class PerfilUsuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE,related_name='fk_perfil_usuario_perfil',db_column='perfil_id')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,related_name='fk_perfil_usuario_usuario',db_column='usuario_id')
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_perfil_usuario',db_column='responsable_id')

    class Meta:
        managed = True
        db_table = 'perfil_usuario'
        unique_together = ('perfil_id','usuario_id',)

    def __str__(self):
        return f'{self.perfil.nombre} - {self.usuario.get_full_name()}'
    
    @property
    def is_perfil_habilitado(self):
        return PerfilUsuarioActivo.objects.filter(perfil=self.perfil,usuario=self.usuario).exists()

    def get_list_perfiles(self,usuario):
        return PerfilUsuario.objects.filter(usuario=usuario).values_list('perfil__nombre',flat=True)
    
    @property
    def perfiles(self):
        return '/'.join(self.get_list_perfiles(self.usuario))

class PerfilUsuarioActivo(models.Model):
    id = models.BigAutoField(primary_key=True)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE,related_name='fk_perfil_perfil_usaurio_activo',db_column='perfil_id')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,related_name='fk_usuario_perfil_usaurio_activo',db_column='usuario_id')
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_usuario_perfil_actibo',db_column='responsable_id')

    class Meta:
        managed = True
        db_table = 'usuario_perfil_activo'
        unique_together = ('perfil_id','usuario_id',)

class Parametro(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    nombre = models.TextField(blank=False, null=False,unique=True)
    metadatos=models.JSONField()

    class Meta:
        managed = True
        db_table = 'parametro'

class ReporteConfigurable(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    nombre = models.TextField(blank=False, null=False)
    codigo_fuente = models.TextField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_reporte_configurable',db_column='responsable_id')

    def __str__(self):
        return f'{self.nombre} {self.tipo_salida_reporte.nombre}'

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        super(ReporteConfigurable, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'reporte_configurable'

class Semestre(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    nombre = models.CharField(max_length=16, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'semestre'

    def __str__(self):
        return f'{self.nombre}'

class Seccion(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    codigo = models.TextField(blank=False, null=False, unique=True)
    semestre = models.ForeignKey(Semestre, models.CASCADE, blank=False, null=False,related_name='fk_seccion_semestre',db_column='semestre_id')
    fecha_desde = models.DateTimeField(blank=False, null=False)
    fecha_hasta = models.DateTimeField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_seccion',db_column='responsable_id')

    def __str__(self):
        return f'{self.codigo} - ({self.semestre} / {self.fecha_desde.year})'

    def get_semestre_nombre(self):
        return f'{self.semestre} / {self.fecha_desde.year}'

    class Meta:
        managed = True
        db_table = 'seccion'

class DocenteSeccion(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,related_name='fk_usuario_docente_seccion',db_column='usuario_id')
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE,related_name='fk_seccion_docente_seccion',db_column='seccion_id')
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_docente_seccion',db_column='responsable_id')

    class Meta:
        managed = True
        db_table = 'docente_seccion'
        unique_together = ('usuario','seccion',)

class AlumnoSeccion(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,related_name='fk_usuario_alumno_seccion',db_column='usuario_id')
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE,related_name='fk_seccion_alumno_seccion',db_column='seccion_id')
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_alumno_seccion',db_column='responsable_id')

    class Meta:
        managed = True
        db_table = 'alumno_seccion'
        unique_together = ('usuario','seccion',)

class TipoEntrada(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    nombre = models.TextField(blank=False, null=False)
    tipo = models.TextField(blank=False, null=False)
    ind_archivo = models.BooleanField(default=False)
    ind_multiple = models.BooleanField(default=False)
    formato = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_tipo_entrada',db_column='responsable_id')
    
    def __str__(self):
        formato = f'({self.formato})' if self.formato and self.formato != '' else ''
        return f'{self.nombre} {formato}'

    class Meta:
        managed = True
        db_table = 'tipo_entrada'

class Actividad(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    actividad_padre = models.ForeignKey('self',on_delete=models.CASCADE, related_name='fk_actividad_padre_actividad',blank=True, null=True,db_column='actividad_padre_id')
    nombre = models.TextField(blank=False, null=False)
    descripcion = models.TextField(blank=True, null=True)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE,related_name='fk_seccion_actividad',db_column='seccion_id')
    tipo_entrada = models.ForeignKey(TipoEntrada, on_delete=models.CASCADE,blank=True, null=True,related_name='fk_tipo_entrada_actividad',db_column='tipo_entrada_id')
    orden = models.IntegerField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_actividad',db_column='responsable_id')

    def __str__(self):
        return f"{self.orden_formateado} {self.nombre}"
    
    @property
    def depende_de(self):
        if self.is_nieto:
            return f"{self.actividad_padre.actividad_padre.orden}.{self.actividad_padre.orden}. {self.actividad_padre.nombre}"
        elif self.is_hijo:
            return f"{self.actividad_padre.orden}. {self.actividad_padre.nombre}"
        else:
            return "-"
    
    @property
    def is_nieto(self):
        if self.actividad_padre and self.actividad_padre.actividad_padre:
            return True
        return False
    
    @property
    def is_hijo(self):
        if self.actividad_padre:
            return True
        return False
        
    @property
    def is_padre(self):
        if self.fk_actividad_padre_actividad.all().count()>0:
            return True
        return False
    
    @property
    def is_abuelo(self):
        if self.is_padre and self.fk_actividad_padre_actividad.last().is_padre:
            if self.fk_actividad_padre_actividad.all().count()>0:
                return True
        return False

    @property
    def orden_formateado(self):
        if self.is_nieto:
            abuelo = self.actividad_padre.actividad_padre.orden
            padre = self.actividad_padre.orden
            return f"{abuelo}.{padre}.{self.orden}."
        elif self.is_hijo:
            padre = self.actividad_padre.orden
            return f"{padre}.{self.orden}."
        else:
            return f"{self.orden}."

    class Meta:
        managed = True
        db_table = 'actividad'

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        self.descripcion = self.descripcion.strip().upper()
        super(Actividad, self).save(*args, **kwargs)

class ActividadRespuestaUsuario(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE,related_name='fk_actividad_actividad_respuesta_usuario',db_column='actividad_id')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,related_name='fk_usuario_actividad_respuesta_usuario',db_column='usuario_id')
    respuesta = models.TextField(blank=False, null=False)
    ind_publicada = models.BooleanField(default=True)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_actividad_respuesta_usuario',db_column='responsable_id')
    
    class Meta:
        managed = True
        db_table = 'actividad_respuesta_usuario'
        unique_together = ('actividad','usuario','respuesta',)

class BitacoraActividadRespuestaUsuario(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    bitacora_padre = models.ForeignKey('self',on_delete=models.CASCADE,blank=True, null=True,related_name='fk_bitacora_padre_bitacora_actividad_respuesta_usuario',db_column='bitacora_padre_id')
    actividad_respuesta_usuario = models.ForeignKey(ActividadRespuestaUsuario, on_delete=models.CASCADE,related_name='fk_actividad_respuesta_usuario_bitacora_actividad_respuesta_usuario',db_column='actividad_respuesta_usuario_id')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,related_name='fk_usuario_bitacora_actividad_respuesta_usuario',db_column='usuario_id')
    comentario = models.TextField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_bitacora_actividad_respuesta_usuario',db_column='responsable_id')

    class Meta:
        managed = True
        db_table = 'bitacora_actividad_respuesta_usuario'

class TipoDocumento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.TextField(blank=False, null=False)
    mnemonico = models.CharField(max_length=10, blank=False, null=False)
    folio_correlativo = models.IntegerField(blank=False, null=False)
    ruta = models.TextField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_tipo_documento',db_column='responsable_id')

    class Meta:
        managed = True
        db_table = 'tipo_documento'

    def __str__(self):
        return self.nombre

class EstadoDocumento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_estado_documento',db_column='responsable_id')

    class Meta:
        managed = True
        db_table = 'estado_documento'
    
    def __str__(self):
        return self.nombre

class Documento(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    folio = models.TextField(blank=False, null=False)
    nombre = models.TextField(blank=False, null=False)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE,related_name='fk_tipo_documento_documento',db_column='tipo_documento_id')
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_documento',db_column='responsable_id')

    class Meta:
        managed = True
        db_table = 'documento'

    def __str__(self):
        return f'''{self.folio}-{self.nombre}'''

    def get_folio(self):
        correlativo_actual = 1
        if self.tipo_documento.folio_correlativo is not None:
            correlativo_actual = self.tipo_documento.folio_correlativo + 1
        self.tipo_documento.folio_correlativo = correlativo_actual
        self.tipo_documento.save()
        return f'{self.tipo_documento.mnemonico}{correlativo_actual:09}'

    def save(self, *args, **kwargs):
        folio = self.get_folio()
        self.doc_folio = folio
        self.doc_nombre = f'{folio}.pdf'
        return super(Documento, self).save(*args, **kwargs)
    
class VersionDocumento(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    version = models.IntegerField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now=True)
    metadatos=models.JSONField()
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE,related_name='fk_documento_version_documento',db_column='documento_id')
    ruta = models.TextField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_version_documento',db_column='responsable_id')

    class Meta:
        managed = True
        db_table = 'version_documento'

    def __str__(self):
        return f'''{self.documento.folio}-{self.documento.nombre}-(v{self.version})'''

    
