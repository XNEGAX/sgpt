import json
from django.db import models
from django.contrib.auth.models import User
from apps.log.views import LogManager

class Sexo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=9, unique=True)
    acronimo = models.CharField(max_length=1,verbose_name='Acrónimo', unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_sexo')

    class Meta:
        managed = True
        db_table = 'sexo'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        self.acronimo = self.acronimo.strip().upper()
        super(Sexo, self).save(*args, **kwargs)

class EstadoCivil(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=10, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_estado_civil')

    class Meta:
        managed = True
        db_table = 'estado_civil'

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        super(EstadoCivil, self).save(*args, **kwargs)

class Nacionalidad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.TextField(unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_nacionalidad')

    class Meta:
        managed = True
        db_table = 'nacionalidad'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        super(Nacionalidad, self).save(*args, **kwargs)
    
class TipoModulo(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField(blank=False, null=False, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_tipo_modulo')

    def set_peticion(self, x):
        self.peticion = json.dumps(x)

    def get_peticion(self):
        return json.loads(self.peticion)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        super(TipoModulo, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'tipo_modulo'
        

class Modulo(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField(blank=False, null=False)
    url = models.TextField(blank=False, null=False)
    modulo_padre = models.ForeignKey('self',on_delete=models.CASCADE, related_name='relacion_modulo_padre',blank=True, null=True)
    icono = models.TextField(blank=True, null=True)
    orden = models.IntegerField(blank=False, null=False)
    tipo_modulo = models.ForeignKey(TipoModulo, models.CASCADE, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_modulo')

    class Meta:
        managed = True
        db_table = 'modulo'
    
    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        self.url = self.url.strip()
        super(Modulo, self).save(*args, **kwargs)

class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.TextField(blank=False, null=False, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_rol')

    class Meta:
        managed = True
        db_table = 'rol'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        super(Rol, self).save(*args, **kwargs)

class ModuloRol(models.Model):
    id = models.BigAutoField(primary_key=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE,related_name="modulorol_set")
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_modulo_rol')

    class Meta:
        managed = True
        db_table = 'modulo_rol'

class Perfil(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField(blank=False, null=False, unique=True)
    editable = models.BooleanField(default=True)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_perfil')

    class Meta:
        managed = True
        db_table = 'perfil'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        super(Perfil, self).save(*args, **kwargs)

class UsuarioPerfilActivo(models.Model):
    id = models.BigAutoField(primary_key=True)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE,related_name='usuarioperfilactivo_set')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_usuario_perfil_actibo')

    class Meta:
        managed = True
        db_table = 'usuario_perfil_activo'

class PerfilRol(models.Model):
    id = models.BigAutoField(primary_key=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_perfil_rol')

    class Meta:
        managed = True
        db_table = 'perfil_rol'

class UsuarioPerfilRol(models.Model):
    id = models.BigAutoField(primary_key=True)
    perfil_rol = models.ForeignKey(PerfilRol, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    permiso = models.JSONField()
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='responsable_crud_usuario_perfil_rol')

    def set_permiso(self, x):
        self.permiso = json.dumps(x)

    def get_permiso(self):
        return json.loads(self.permiso)

    def save(self, *args, **kwargs):
        self.permiso = json.loads(self.permiso.strip())
        super(UsuarioPerfilRol, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'usuario_perfil_rol'