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
    modulo_padre = models.ForeignKey('self',on_delete=models.CASCADE, related_name='relacion_modulo_padre',blank=True, null=True)
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
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE,related_name='perfil_modulo_perfil')
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE,related_name='perfil_modulo_modulo')

    class Meta:
        managed = True
        db_table = 'perfil_modulo'
        unique_together = ('perfil_id', 'modulo_id',)

class PerfilUsuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE,related_name='perfil_usuario_perfil')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,related_name='perfil_usuario_usuario')
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_perfil_usuario')

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
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE,related_name='usuario_perfil_activo_perfil')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_usuario_perfil_actibo')

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
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_reporte_configurable')

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
    semestre = models.ForeignKey(Semestre, models.CASCADE, blank=False, null=False,related_name='seccion_semestre')
    fecha_desde = models.DateTimeField(blank=False, null=False)
    fecha_hasta = models.DateTimeField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_seccion')

    def __str__(self):
        return f'{self.codigo} - ({self.semestre} / {self.fecha_desde.year})'

    def get_semestre_nombre(self):
        return f'{self.semestre} / {self.fecha_desde.year}'

    class Meta:
        managed = True
        db_table = 'seccion'

class DocenteSeccion(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_docente_seccion')

    class Meta:
        managed = True
        db_table = 'docente_seccion'
        unique_together = ('usuario','seccion',)

class AlumnoSeccion(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_alumno_seccion')

    class Meta:
        managed = True
        db_table = 'alumno_seccion'
        unique_together = ('usuario','seccion',)

class Fase(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    nombre = models.TextField(blank=False, null=False, unique=True)
    descripcion = models.TextField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_fase')
    
    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'fase'

class TipoEntrada(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    nombre = models.TextField(blank=False, null=False)
    ind_archivo = models.BooleanField(default=False)
    formato = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_tipo_entrada')
    
    def __str__(self):
        formato = f'({self.formato})' if self.formato and self.formato != '' else ''
        return f'{self.nombre} {formato}'

    class Meta:
        managed = True
        db_table = 'tipo_entrada'

class Actividad(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    nombre = models.TextField(blank=False, null=False)
    descripcion = models.TextField(blank=False, null=False)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE,blank=True, null=True)
    tipo_entrada = models.ForeignKey(TipoEntrada, on_delete=models.CASCADE)
    orden = models.IntegerField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_actividad')

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'actividad'

class ActividadRespuestaUsuario(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    seccion_configuracion = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    respuesta = models.TextField(blank=False, null=False)
    ind_publicada = models.BooleanField(default=True)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_actividad_respuesta_usuario')
    
    class Meta:
        managed = True
        db_table = 'actividad_respuesta_usuario'
        unique_together = ('seccion_configuracion','usuario','respuesta',)

class BitacoraActividadRespuestaUsuario(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    bitacora_padre = models.ForeignKey('self',on_delete=models.CASCADE,blank=True, null=True)
    actividad_respuesta_usuario = models.ForeignKey(ActividadRespuestaUsuario, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_bitacora_actividad_respuesta_usuario')

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
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_tipo_documento')

    class Meta:
        managed = True
        db_table = 'tipo_documento'

    def __str__(self):
        return self.nombre

class EstadoDocumento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_estado_documento')

    class Meta:
        managed = True
        db_table = 'estado_documento'
    
    def __str__(self):
        return self.nombre

class Documento(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    folio = models.TextField(blank=False, null=False)
    nombre = models.TextField(blank=False, null=False)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_documento')

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
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    ruta = models.TextField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_version_documento')

    class Meta:
        managed = True
        db_table = 'version_documento'

    def __str__(self):
        return f'''{self.documento.folio}-{self.documento.nombre}-(v{self.version})'''

    
