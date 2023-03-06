from proyecto.log import LogManager
import json
import gantt
import base64
import os
from django.db import models
from django.contrib.auth.models import User
from function import formatear_error
from function import ConsultaBD
from datetime import datetime
from datetime import date
from function import getDatetime
from function.gantt import CustomProject
 
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

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        self.metadatos = json.dumps(self.metadatos)
        super(Parametro, self).save(*args, **kwargs)

    def get_metadatos(self):
        try:
            return self.metadatos
        except:
            return json.loads(self.metadatos)
    
    def __str__(self):
        return self.nombre

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
    fecha_desde = models.DateField(blank=False, null=False)
    fecha_hasta = models.DateField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_seccion',db_column='responsable_id')

    def __str__(self):
        return f'{self.codigo} - ({self.semestre} / {self.fecha_desde.year})'

    def get_semestre_nombre(self):
        return f'{self.semestre} / {self.fecha_desde.year}'
    
    @property
    def periodo(self):
        return f"{self.fecha_desde.strftime('%d/%m/%Y')} - {self.fecha_hasta.strftime('%d/%m/%Y')}"
    
    @property
    def ind_activa(self):
        return self.fecha_desde.date()<=datetime.now().date() and self.fecha_hasta.date()>=datetime.now().date()
    
    def set_actividad(self,parametros):
        actividad = Actividad(**parametros)
        actividad.save()
        return actividad
    
    def set_configuracion_base(self,tipo,responsable):
        try:
            tipo = 'ACTIVIDADES_BASE_COMPLETA' if int(tipo) == 1 else 'ACTIVIDADES_BASE_MINIMA'
            parametros = Parametro.objects.filter(nombre=tipo).last()
            actividades_abuelas = parametros.get_metadatos()
            for actividad_abuela in actividades_abuelas:
                temp_abuela = dict(actividad_abuela).copy()
                temp_abuela['responsable_id'] = responsable.id
                temp_abuela['seccion_id'] = self.id
                temp_abuela['actividad_padre_id'] =None
                if 'actividades' in temp_abuela:
                    del temp_abuela['actividades']
                if temp_abuela.get('tipo_entrada'):
                    temp_abuela['tipo_entrada_id'] = temp_abuela['tipo_entrada']
                    del temp_abuela['tipo_entrada']
                abuela = self.set_actividad(temp_abuela)

                actividades_padres = actividad_abuela.get('actividades')
                if actividades_padres:
                    for actividad_padre in actividades_padres:
                        temp_padre = actividad_padre.copy()
                        temp_padre['responsable_id'] = responsable.id
                        temp_padre['seccion_id'] = self.id
                        temp_padre['actividad_padre_id'] =abuela.pk
                        if 'actividades' in temp_padre:
                            del temp_padre['actividades']
                        if temp_padre.get('tipo_entrada'):
                            temp_padre['tipo_entrada_id'] = temp_padre['tipo_entrada']
                            del temp_padre['tipo_entrada']
                        padre = self.set_actividad(temp_padre)

                        actividades_hijas = actividad_padre.get('actividades')
                        if actividades_hijas:
                            for actividad_hija in actividades_hijas:
                                temp_hija = actividad_hija.copy()
                                temp_hija['responsable_id'] = responsable.id
                                temp_hija['seccion_id'] = self.id
                                temp_hija['actividad_padre_id'] =padre.pk
                                if temp_hija.get('tipo_entrada'):
                                    temp_hija['tipo_entrada_id'] = temp_hija['tipo_entrada']
                                    del temp_hija['tipo_entrada']
                                self.set_actividad(temp_hija)
            return True
        except Exception as exc:
            print(formatear_error(exc))
            return False

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

    def __str__(self):
        return f'{self.seccion} - prof. {self.usuario.get_full_name()} '
     
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
    ind_base = models.BooleanField(default=False)
    orden = models.IntegerField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_actividad',db_column='responsable_id')

    def __str__(self):
        return f"{self.orden_formateado if not self.ind_base else ''} {self.nombre}"
    
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

    @property
    def respuesta(self):
        return self.fk_actividad_actividad_respuesta_usuario.last()
    
    @property
    def respuesta_formateada(self):
        if self.respuesta:
            if self.respuesta.respuesta and self.tipo_entrada.ind_archivo and self.tipo_entrada.ind_multiple and 'gantt' not in self.nombre.lower():
                respuesta = list(self.respuesta.respuesta)
                for r in respuesta:
                    try:
                        with open(r.get('ruta_archivo'), "rb") as image_file:
                            r['archivo'] = base64.b64encode(image_file.read()).decode('utf-8')
                    except:
                        pass
                    r['orden'] = f"{self.tipo_entrada.nombre.capitalize()} {self.orden_formateado if not self.ind_base else ''}"
                    r['tipo'] = self.tipo_entrada.formato
                return respuesta
        return self.respuesta

    class Meta:
        managed = True
        db_table = 'actividad'
        unique_together = ('actividad_padre', 'seccion','orden',)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        self.descripcion = self.descripcion.strip().upper()
        super(Actividad, self).save(*args, **kwargs)

class AlumnoSeccion(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,related_name='fk_usuario_alumno_seccion',db_column='usuario_id')
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE,related_name='fk_seccion_alumno_seccion',db_column='seccion_id')
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_alumno_seccion',db_column='responsable_id')

    class Meta:
        managed = True
        db_table = 'alumno_seccion'

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.seccion}"

class Proyecto(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    nombre = models.TextField(blank=False, null=False)
    descripcion = models.TextField(blank=False, null=False)
    ind_aprobado = models.BooleanField(blank=True, null=True)
    in_activo = models.BooleanField(blank=False, null=False,default=True)
    motivo_rechazo = models.TextField(blank=True, null=True)
    alumno_seccion = models.OneToOneField(AlumnoSeccion, on_delete=models.CASCADE,related_name='fk_alumno_seccion_proyecto',db_column='alumno_seccion_id')
    fecha_desde =  models.DateField()
    fecha_hasta =  models.DateField()
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_proyecto',db_column='responsable_id')

    class Meta:
        managed = True
        db_table = 'proyecto'

    def __str__(self):
        return self.nombre

    def __unicode__(self):
       return self.nombre
        
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        self.descripcion = self.descripcion.strip().upper()
        self.motivo_rechazo = self.motivo_rechazo if self.motivo_rechazo !='' else None
        super(Proyecto, self).save(*args, **kwargs)
    
    @property
    def periodo(self):
        return f"{self.fecha_desde.strftime('%d/%m/%Y')} - {self.fecha_hasta.strftime('%d/%m/%Y')}"
    
    @property
    def is_pendiente(self):
        return self.ind_aprobado is None
    
    @property
    def is_aprobado(self):
        return self.ind_aprobado is True

    @property
    def is_rechazado(self):
        return self.ind_aprobado is False
    
    @property
    def actividades_seccion(self):
        return self.alumno_seccion.seccion.fk_seccion_actividad.all()
    
    @property
    def cantidad_actividades_seccion(self):
        return len(self.actividades_seccion)
    
    @property
    def actividades_respondida_todas(self):
        return self.fk_proyecto_actividad_respuesta_proyecto.all()
    
    @property
    def cantidad_actividades_respondida_todas(self):
        return len(self.actividades_respondida_todas)

    @property
    def actividades_respondidas_por_publicar(self):
        return self.fk_proyecto_actividad_respuesta_proyecto.filter(ind_publicada=False)

    @property
    def cantidad_actividades_respondidas_por_publicar(self):
        return len(self.actividades_respondidas_por_publicar)
    
    @property
    def actividades_respondidas_publicadas(self):
        return self.fk_proyecto_actividad_respuesta_proyecto.filter(ind_publicada=True)

    @property
    def cantidad_actividades_respondidas_publicadas(self):
        return len(self.actividades_respondidas_publicadas)
    
    @property
    def url(self):
        return f'/alumno/seccion/proyecto/{self.id}/actividades/'
    
    @property
    def actividades_menu(self):
        actividades_padre = []
        actividades_padre_proyecto = self.actividades_seccion.filter(actividad_padre=None).order_by('orden')
        for actividad_padre_proyecto in actividades_padre_proyecto:
            actividades_hijo = []
            actividades_hijo_url = []
            actividades_hijo_proyecto = self.actividades_seccion.filter(actividad_padre=actividad_padre_proyecto.id).order_by('orden')
            for actividad_hijo_proyecto in actividades_hijo_proyecto:
                actividades_hijo_url.append(f'{self.url}?actividad={actividad_hijo_proyecto.id}')
                actividades_hijo.append({
                    'url':f'{self.url}?actividad={actividad_hijo_proyecto.id}',
                    'nombre': actividad_hijo_proyecto.nombre,
                })

            actividades_padre.append({
                'url':f'{self.url}?actividad={actividad_padre_proyecto.id}' if not actividad_padre_proyecto.is_padre else 'javascript:void(0);',
                'is_padre': actividad_padre_proyecto.is_padre,
                'nombre': actividad_padre_proyecto.nombre,
                'actividades_hijo_url':actividades_hijo_url,
                'actividades_hijo':actividades_hijo,
            })
        return actividades_padre
    
    def set_gantt(self,archivo):
        actividad = self.actividades_seccion.filter(nombre__icontains='gantt').last()
        if actividad:
            respuesta = ActividadRespuestaProyecto.objects.filter(
                proyecto=self,
                actividad=actividad
            )
            if respuesta.exists():
                respuesta.update(
                    respuesta = archivo,
                )
            else:
                obj = ActividadRespuestaProyecto(
                    proyecto = self,
                    actividad = actividad,
                    respuesta = archivo,
                    responsable_id = 0,
                    ind_publicada = True
                )
                obj.save()
                return True
        return False

    @property
    def archivo_existe(self):
        path = f'proyecto/gantt/{self.id}.svg'
        if not os.path.exists(path):
            False
        return True
    
    @property
    def ruta(self):
        path = 'proyecto/gantt/'
        if not os.path.exists(path):
            os.makedirs(path)
        return f'{path}{self.id}.svg'
    
    @property
    def tareas(self):
        return self.fk_proyecto_gantt.all()

    @property
    def gantt(self):
        gantt.define_font_attributes(fill='black', stroke='black', stroke_width=0, font_family="Verdana")
        p = CustomProject(color='#35C367')
        tareas = self.tareas
        if len(tareas)>0:
            for tarea in self.tareas:
                p.add_task(gantt.Task(name=tarea.nombre, start=tarea.fecha_inicio, duration=tarea.duration))
        else:
            p.add_task(gantt.Task(name=self.nombre, start=self.fecha_desde, duration=1))
        p.make_svg_for_tasks(filename=self.ruta, today=getDatetime(), start=self.fecha_desde, end=self.fecha_hasta)
        self.set_gantt(self.ruta)
        with open(self.ruta, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')


class ActividadRespuestaProyecto(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE,related_name='fk_proyecto_actividad_respuesta_proyecto',db_column='proyecto_id')
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE,related_name='fk_actividad_actividad_respuesta_usuario',db_column='actividad_id')
    respuesta = models.JSONField(blank=False, null=False)
    ind_publicada = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_actividad_respuesta_usuario',db_column='responsable_id')
    
    class Meta:
        managed = True
        db_table = 'actividad_respuesta_proyecto'
        unique_together = ('proyecto','actividad','respuesta',)

    def save(self, *args, **kwargs):
        if self.actividad.tipo_entrada.ind_archivo and self.actividad.tipo_entrada.ind_multiple:
            update = kwargs.get('update')
            if not update:
                archivo = kwargs.get('archivo')
                nombre = kwargs.get('nombre')
                self.respuesta = self.subir_archivo(archivo,nombre)
            kwargs = {}
        super(ActividadRespuestaProyecto, self).save(*args, **kwargs)

    def subir_archivo(self,data,nombre):
        archivos = []
        if self.respuesta:
            archivos = list(self.respuesta)
        # generamos la ruta si esta no existe
        ruta = f'media/proyecto/{self.proyecto.id}/actividad/{self.actividad.id}/'
        if not os.path.exists(ruta):
            os.makedirs(ruta)
        # obtenemos la extencion y el nuevo nombre del archivo
        if self.actividad.tipo_entrada.formato =='pdf':
            file_name = f'{nombre}.pdf'
        else:
            temp_name = data.name.split('.')
            file_name = ''
            if isinstance(temp_name, list):
                for extension in temp_name:
                    file_name = f'{nombre}.{extension}'  
        # subimos el archivo
        ruta_archivo = f'{ruta}{file_name}'
        open(ruta_archivo, 'wb').write(data.file.read())
        # validamos si ya existe uno con el mismo nombre
        existe = False
        for archivo in archivos:
            if archivo.get('nombre').upper() == nombre.upper():
                archivo['ruta_archivo'] = ruta_archivo
                existe= True
        print(existe)
        if not existe:
            archivos.append({
                'nombre':nombre.upper(),
                'ruta_archivo':ruta_archivo
            })
        return archivos

class BitacoraActividadRespuestaProyecto(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    bitacora_padre = models.ForeignKey('self',on_delete=models.CASCADE,blank=True, null=True,related_name='fk_bitacora_padre_bitacora_actividad_respuesta_proyecto',db_column='bitacora_padre_id')
    actividad_respuesta_proyecto = models.ForeignKey(ActividadRespuestaProyecto, on_delete=models.CASCADE,related_name='fk_actividad_respuesta_proyecto_bitacora_actividad_respuesta_proyecto',db_column='actividad_respuesta_proyecto_id')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,related_name='fk_usuario_bitacora_actividad_respuesta_proyecto',db_column='usuario_id')
    comentario = models.TextField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_bitacora_actividad_respuesta_proyecto',db_column='responsable_id')

    class Meta:
        managed = True
        db_table = 'bitacora_actividad_respuesta_proyecto'

class Gantt(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE,related_name='fk_proyecto_gantt',db_column='proyecto_id')
    nombre = models.TextField(blank=False, null=False)
    fecha_inicio =  models.DateField()
    fecha_termino =  models.DateField()
    duration = models.IntegerField(blank=False, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_gantt',db_column='responsable_id')

    class Meta:
        managed = True
        db_table = 'gantt'

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().upper()
        diferencia = self.fecha_termino - self.fecha_inicio
        self.duration = diferencia.days
        super(Gantt, self).save(*args, **kwargs)

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

    
