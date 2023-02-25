from django.db import models
from django.db.models.signals import post_save, post_delete
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db.models.base import ModelState
from django.dispatch import receiver
from proyecto.models.log import Log
from django.forms.models import model_to_dict
from datetime import date,datetime

def format(instance,**kwargs):
    metadata = {}
    modelo = ContentType.objects.filter(model=instance._meta.db_table.replace('_','')).last()
    if type(instance) not in (Log,ModelState,LogEntry,Site)  and 'Migration' not in str(type(instance)) and modelo:
        print(instance)
        metadata = instance.__dict__
        metadata["detalle"] = str(model_to_dict(instance))
        for k,v in metadata.items():
            if isinstance(v,(date,datetime)):
                metadata[k] = metadata.get(k).strftime("%Y-%m-%d %H:%M:%S")
        if metadata.get('_state'):
            del metadata["_state"]
    return (modelo,metadata)

class LogManager(models.Model):
    @receiver(post_save)
    def log_save(sender, instance,**kwargs):
        accion = 1 if kwargs.get('created') else 2
        data = format(instance,**kwargs)
        if len(data)>0 and bool(data[1]):
            Log(modelo=data[0],accion=accion,fecha = data[1].get('fecha'),responsable_id=data[1].get('responsable_id'),metadatos=data[1]).save()
            
    @receiver(post_delete)
    def log_save(sender, instance,**kwargs):
        accion = 3
        data = format(instance,**kwargs)
        if len(data)>0 and bool(data[1]):
            Log(modelo=data[0],accion=accion,fecha = data[1].get('fecha'),responsable_id=data[1].get('responsable_id'),metadatos=data[1]).save()

    class Meta:
        managed = False
        abstract = True
