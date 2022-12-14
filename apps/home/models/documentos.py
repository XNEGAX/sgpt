from apps.log.views import LogManager
import json
from django.db import models
from django.contrib.auth.models import User

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
    estado_documento = models.ForeignKey(EstadoDocumento, on_delete=models.CASCADE)
    ruta = models.TextField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_version_documento')

    class Meta:
        managed = True
        db_table = 'version_documento'

    def __str__(self):
        return f'''{self.documento.folio}-{self.documento.nombre}-(v{self.version})'''