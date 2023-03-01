from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from dateutil import parser
from function import is_date
from django.core import serializers
import datetime
import json
from dateutil import tz

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
        metadata = serializers.deserialize('json', log_data.get('detalle'))
        for deserialized_object in metadata:
            return deserialized_object.object