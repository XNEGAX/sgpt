import json
from django.db import models
from django.contrib.auth.models import User
from apps.log.views import LogManager
from django.contrib.contenttypes.models import ContentType

class Parametro(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    nombre = models.TextField(blank=False, null=False,unique=True)
    metadatos=models.JSONField()
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_parametro')

    class Meta:
        managed = True
        db_table = 'parametro'

class ConfiguracionBase(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    modelo = models.ForeignKey(ContentType,models.SET_NULL,blank=True,null=True)
    metadatos=models.JSONField()
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_configuracionbase')

    def get_fields(self):
        campos = []
        exec(f'campos = list({self.modelo}._meta.get_fields())')
        return campos

    class Meta:
        managed = True
        db_table = 'configuracion_base'

class TipoSalidaReporte(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    nombre = models.TextField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_tipo_salida_reporte')

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        super(TipoSalidaReporte, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'tipo_salida_reporte'

class ReporteConfigurable(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    nombre = models.TextField(blank=False, null=False)
    codigo_fuente = models.TextField(blank=False, null=False)
    tipo_salida_reporte = models.ForeignKey(TipoSalidaReporte, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_reporte_configurable')

    def __str__(self):
        return f'{self.nombre} {self.tipo_salida_reporte.nombre}'

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        super(TipoSalidaReporte, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'reporte_configurable'

class Seccion(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    codigo = models.TextField(blank=False, null=False)
    nombre = models.TextField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_seccion')

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        super(Seccion, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'seccion'

class Fase(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    nombre = models.TextField(blank=False, null=False)
    descripcion = models.TextField(blank=False, null=False)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_fase')
    
    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        self.descripcion = self.descripcion.strip()
        super(Seccion, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'fase'

class Actividad(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    nombre = models.TextField(blank=False, null=False)
    descripcion = models.TextField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_actividad')

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        self.descripcion = self.descripcion.strip()
        super(Actividad, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'actividad'

class TipoEntrada(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    tipo = models.TextField(blank=False, null=False)
    ind_archivo = models.BooleanField(default=True)
    formato = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_tipo_entrada')
    
    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.tipo = self.tipo.strip().lower()
        self.formato = self.descripcion.strip()
        super(Actividad, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'tipo_entrada'

class FaseActividadTipoEntrada(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    tipo_entrada = models.ForeignKey(TipoEntrada, on_delete=models.CASCADE)
    orden = models.IntegerField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_face_actividad_tipo_entrada')

    class Meta:
        managed = True
        db_table = 'fase_actividad_tipo_entrada'
    
class FaseActividadRespuestaEntrada(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    fase_actividad_tipo_entrada = models.ForeignKey(FaseActividadTipoEntrada, on_delete=models.CASCADE)
    respuesta = models.TextField(blank=False, null=False)
    orden = models.IntegerField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_face_actividad_respuesta_entrada')

    def get_respuesta(self):
        return json.loads(self.respuesta)

    class Meta:
        managed = True
        db_table = 'fase_actividad_respuesta_entrada'

class FaseActividadRespuestaUsuario(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    fase_actividad_tipo_entrada = models.ForeignKey(FaseActividadTipoEntrada, on_delete=models.CASCADE)
    respuesta = models.TextField(blank=False, null=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ind_publicada = models.BooleanField(default=True)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_face_actividad_respuesta_usuario')

    def get_respuesta(self):
        return json.loads(self.respuesta)
    
    class Meta:
        managed = True
        db_table = 'fase_actividad_respuesta_persona'

class BitacoraFaseActividadRespuestaUsuario(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    bitacora_padre = models.ForeignKey('self',on_delete=models.CASCADE,blank=True, null=True)
    fase_actividad_respuesta_persona = models.ForeignKey(FaseActividadRespuestaUsuario, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_bitacora_face_actividad_respuesta_usuario')

    class Meta:
        managed = True
        db_table = 'bitacora_fase_actividad_respuesta_persona'