from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

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
