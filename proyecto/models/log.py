from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
from function import formatear_error
from dateutil import parser
from function import is_date
import datetime

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
    def table_name(self):
        loc = {}
        code = f"""
from {self.modelo.app_label}.models import {self.model_name}
table_name = {self.model_name}._meta.db_table
        """
        exec(code,globals(),loc)
        return loc['table_name']
    
    @property
    def model_name(self):
        return self.modelo.model.title()
    
    @property
    def fields(self):
        loc = {}
        code = f"""
from {self.modelo.app_label}.models import {self.model_name}
fields = []
for f in {self.model_name}._meta.get_fields():
    if 'fk' not in f.name:
        if hasattr(f, 'db_column') and f.db_column:
            fields.append(f.db_column)
        else:
            fields.append(f.name)
        """
        exec(code,globals(),loc)
        return loc['fields']
            
    @property
    def data(self):
        log_data = dict(self.metadatos)
        metadata = eval(log_data.get('detalle'))
        log_data.update(metadata)
        for item in list(log_data):
            if item not in self.fields:
                del log_data[item]
        for k,v in log_data.items():
            if isinstance(v,str) and is_date(v):
                log_data[k] = parser.parse(v)
                print(parser.parse(v)) 
        return log_data

    @property  
    def instancia_recuperada(self):
        loc = {}
        code = f"""
from {self.modelo.app_label}.models import {self.model_name}
instancia = {self.model_name}(**{self.data})
        """
        exec(code,globals(),loc)
        return loc['instancia']