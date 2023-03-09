from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core import serializers
import json
from dateutil import tz
from proyecto.models import *



def tzlocal():
    return tz.gettz('America / Chile')

class Log(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    modelo = models.ForeignKey(ContentType,models.CASCADE,blank=False,null=False)
    accion = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='autor_log')
    metadatos=models.JSONField()

    class Meta:
        managed = True
        db_table = 'log'

    def get_fields(self):
        campos = []
        exec(f'campos = list({self.modelo}._meta.get_fields())')
        return campos

    @property
    def accion_nombre(self):
        if self.accion == 1:
            return 'Creación'
        elif self.accion == 2:
            return 'Modificación'
        else:
            return 'Eliminación'

    @property  
    def instancia_recuperada(self):
        log_data = json.loads(self.metadatos)
        metadata = list(serializers.deserialize('json', log_data.get('detalle')))
        for deserialized_object in metadata:
            if self.accion in (1,2):
                return deserialized_object.object
            dictcionario = deserialized_object.object.__dict__

            if dictcionario.get('codigo'):
                return dictcionario.get('codigo')
            elif dictcionario.get('nombre'):
                return dictcionario.get('codigo')
            else:
                cadena = {}
                for k,v in dictcionario.items():
                    if k in ('perfil_id','usuario_id','semestre_id','actividad_padre_id','tipo_entrada_id','seccion_id','alumno_seccion_id','proyecto_id','actividad_id','bitacora_padre_id','actividad_respuesta_proyecto_id','tipo_documento_id','documento_id'):
                        cadena[k]=v
                return f'Relación {str(tuple(cadena.items()))}'.upper()
            