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

    def __unicode__(self):
       return self.nombre
    
    def __str__(self):
        return self.nombre

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
    
class Documento(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_documento',db_column='responsable_id')

    class Meta:
        managed = True
        db_table = 'documento'

    def get_folio(self):
        return f'pry-{self.id}'
    
    def __unicode__(self):
       return self.get_folio()

    def __str__(self):
        return self.get_folio()

    
    
class VersionDocumento(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    version = models.IntegerField(blank=False, null=False)
    metadatos = models.TextField(blank=False, null=False)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE,related_name='fk_documento_version_documento',db_column='documento_id')
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_version_documento',db_column='responsable_id')

    class Meta:
        managed = True
        db_table = 'version_documento'

    def __str__(self):
        return f'''{self.documento.get_folio()} (v{self.version})'''
    
    def save(self, *args, **kwargs):
        self.version = 0
        anterior = VersionDocumento.objects.filter(documento=self.documento).order_by('-version').last()
        if anterior:
            self.version = anterior.version
        self.version += 1
        return super(VersionDocumento, self).save(*args, **kwargs)


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


    @property
    def meses_duracion_nombre(self):
        from dateutil.relativedelta import relativedelta
        from function import mes_nombre_completo
        data= []
        temp_inicio = self.fecha_desde
        while temp_inicio<self.fecha_hasta:
            data.append(mes_nombre_completo[temp_inicio.strftime('%B').lower()])
            temp_inicio+= relativedelta(months=1)
        return data

    @property
    def meses_duracion_numero(self):
        from dateutil.relativedelta import relativedelta
        data= []
        temp_inicio = self.fecha_desde
        while temp_inicio<self.fecha_hasta:
            data.append(temp_inicio.month)
            temp_inicio+= relativedelta(months=1)
        return data

    @property
    def dias_duracion(self):
        return (self.fecha_hasta - self.fecha_desde).days
    
    @property
    def dias_cumplidos(self):
        return (getDatetime().date() - self.fecha_desde).days
    
    @property
    def horas_cumplidas(self):
        return self.dias_cumplidos * 24
    
    @property
    def horas_duracion(self):
        return self.dias_duracion * 24
    
    @property
    def tiempo_esperado_actividad(self):
        cantidad_actividades = self.cantidad_actividades_seccion_para_responder
        if self.horas_duracion>0 and cantidad_actividades>0:
            return self.horas_duracion / cantidad_actividades
        return 0
    
    @property
    def actividades_seccion(self):
        return self.fk_seccion_actividad.all()
    
    @property
    def cantidad_actividades_seccion_para_responder(self):
        cantidad_sin_respuesta = 0
        padres = self.actividades_seccion.filter(actividad_padre__isnull=True,ind_base=False)
        for padre in padres:
            if not padre.is_padre and not padre.is_abuelo:
                cantidad_sin_respuesta += 1
            else:
                hijas = self.actividades_seccion.filter(actividad_padre=padre)
                for hija in hijas:
                    if not hija.is_padre:
                        cantidad_sin_respuesta += 1
                    else:
                        cantidad_sin_respuesta += len(self.actividades_seccion.filter(actividad_padre=hija))
        return cantidad_sin_respuesta
    
    @property
    def cantidad_actividades_seccion_para_responder_totales(self):
        return self.cantidad_actividades_seccion_para_responder * len(self.fk_seccion_alumno_seccion.all())
    
    @property
    def cantidad_actividades_seccion_respondidas(self):
        cantidad_con_respuesta = 0
        for alumno_seccion in self.fk_seccion_alumno_seccion.all():
            proyecto = Proyecto.objects.filter(alumno_seccion=alumno_seccion).last()
            if proyecto:
                cantidad_con_respuesta += len(proyecto.actividades_respondida_todas.filter(actividad__ind_base=False))
        return cantidad_con_respuesta
    
    @property
    def porcentaje_avance(self):
        if self.cantidad_actividades_seccion_para_responder_totales>0:
            return"{:.1f}".format((self.cantidad_actividades_seccion_respondidas*100)/self.cantidad_actividades_seccion_para_responder_totales)
        return 0
    
    @property
    def avance_x_captulo(self):
        data = []
        padres = self.actividades_seccion.filter(actividad_padre__isnull=True,ind_base=False).order_by('orden')
        for padre in padres:
            pendientes = 0
            respondidas = 0
            if not padre.is_padre and not padre.is_abuelo:
                pendientes += 1
                respondidas += len(ActividadRespuestaProyecto.objects.filter(proyecto__alumno_seccion__seccion=self,actividad=padre))
            else:
                hijas = self.actividades_seccion.filter(actividad_padre=padre)
                for hija in hijas:
                    if not hija.is_padre:
                        pendientes += 1
                        respondidas += len(ActividadRespuestaProyecto.objects.filter(proyecto__alumno_seccion__seccion=self,actividad=hija))
                    else:
                        pendientes += len(self.actividades_seccion.filter(actividad_padre=hija))
                        nietas = self.actividades_seccion.filter(actividad_padre=hija)
                        for nieta in nietas:
                            respondidas += len(ActividadRespuestaProyecto.objects.filter(proyecto__alumno_seccion__seccion=self,actividad=nieta))


            data.append({
                'nombre': padre.nombre,
                'pendientes':pendientes * len(self.fk_seccion_alumno_seccion.all()),
                'respondidas':respondidas,
            })

        return data


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
                respuesta =  list(eval(self.respuesta.respuesta))
                for r in respuesta:
                    try:
                        with open(r.get('ruta_archivo'), "rb") as image_file:
                            r['archivo'] = base64.b64encode(image_file.read()).decode('utf-8')
                    except:
                        pass
                    print(f"{self.tipo_entrada.nombre.capitalize()} {self.orden_formateado if not self.ind_base else ''}")
                    r['orden'] = f"{self.tipo_entrada.nombre.capitalize()} {self.orden_formateado if not self.ind_base else ''}"
                    r['tipo'] = self.tipo_entrada.formato
                return respuesta
        return self.respuesta
    

    class Meta:
        managed = True
        db_table = 'actividad'

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
    documento = models.OneToOneField(Documento,blank=True,null=True,on_delete=models.CASCADE,related_name='fk_proyecto_documento',db_column='documento_id')
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
    def url_docente(self):
        return f'/proyecto/{self.id}/informe/detalle/'
    
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
    
    @property
    def actividades_menu_docente(self):
        actividades_padre = []
        actividades_padre_proyecto = self.actividades_seccion.filter(actividad_padre=None).order_by('orden')
        for actividad_padre_proyecto in actividades_padre_proyecto:
            actividades_hijo = []
            actividades_hijo_url = []
            actividades_hijo_proyecto = self.actividades_seccion.filter(actividad_padre=actividad_padre_proyecto.id).order_by('orden')
            for actividad_hijo_proyecto in actividades_hijo_proyecto:
                actividades_hijo_url.append(f'{self.url_docente}?actividad={actividad_hijo_proyecto.id}')
                actividades_hijo.append({
                    'url':f'{self.url_docente}?actividad={actividad_hijo_proyecto.id}',
                    'nombre': actividad_hijo_proyecto.nombre,
                })

            actividades_padre.append({
                'url':f'{self.url_docente}?actividad={actividad_padre_proyecto.id}' if not actividad_padre_proyecto.is_padre else 'javascript:void(0);',
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
                obj.save(**{'update':1})
                return True
        return False

    @property
    def archivo_existe(self):
        path = f'proyecto/gantt/{self.id}.svg'
        if not os.path.exists(path):
            False
        return True
    
    @property
    def ruta_svg(self):
        path = 'proyecto/gantt/'
        if not os.path.exists(path):
            os.makedirs(path)
        return f'{path}{self.id}.svg'
    
    @property
    def ruta_png(self):
        path = 'proyecto/gantt/'
        if not os.path.exists(path):
            os.makedirs(path)
        return f'{path}{self.id}.png'
    
    @property
    def tareas(self):
        return self.fk_proyecto_gantt.all()

    @property
    def gantt(self):
        from dateutil.relativedelta import relativedelta
        try:
            gantt.define_font_attributes(fill='black', stroke='black', stroke_width=0, font_family="Verdana")
            p = CustomProject(color='#35C367')
            tareas = self.tareas
            if len(tareas)>0:
                for tarea in self.tareas:
                    p.add_task(gantt.Task(name=tarea.nombre, start=tarea.fecha_inicio, duration=tarea.duration+1))
            else:
                p.add_task(gantt.Task(name=self.nombre, start=self.fecha_desde, duration=1))
            p.make_svg_for_tasks(filename=self.ruta_svg, today=getDatetime(), start=self.fecha_desde, end=tareas.last().fecha_termino + relativedelta(days=20) if tareas.last() else self.fecha_hasta)

            self.set_gantt(self.ruta_svg)
            with open(self.ruta_svg, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            with open('proyecto/gantt/default.svg', "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        
    @property
    def porcentaje_avance(self):
        cantidad_sin_respuesta = 0
        cantidad_con_respuesta = len(self.actividades_respondida_todas.filter(actividad__ind_base=False))
        padres = self.actividades_seccion.filter(actividad_padre__isnull=True,ind_base=False)
        for padre in padres:
            if not padre.is_padre and not padre.is_abuelo:
                cantidad_sin_respuesta += 1
            else:
                hijas = self.actividades_seccion.filter(actividad_padre=padre)
                for hija in hijas:
                    if not hija.is_padre:
                        cantidad_sin_respuesta += 1
                    else:
                        cantidad_sin_respuesta += len(self.actividades_seccion.filter(actividad_padre=hija))

        if cantidad_sin_respuesta>0:
            return"{:.1f}".format((cantidad_con_respuesta*100)/cantidad_sin_respuesta)
        return 0
    
    @property
    def avance_x_captulo(self):
        data = []
        padres = self.actividades_seccion.filter(actividad_padre__isnull=True,ind_base=False).order_by('orden')
        for padre in padres:
            pendientes = 0
            respondidas = 0
            if not padre.is_padre and not padre.is_abuelo:
                pendientes += 1
                respondidas += len(self.actividades_respondida_todas.filter(actividad=padre))
            else:
                hijas = self.actividades_seccion.filter(actividad_padre=padre)
                for hija in hijas:
                    if not hija.is_padre:
                        pendientes += 1
                        respondidas += len(self.actividades_respondida_todas.filter(actividad=hija))
                    else:
                        pendientes += len(self.actividades_seccion.filter(actividad_padre=hija))
                        nietas = self.actividades_seccion.filter(actividad_padre=hija)
                        for nieta in nietas:
                            respondidas += len(self.actividades_respondida_todas.filter(actividad=nieta))


            data.append({
                'nombre': padre.nombre,
                'pendientes':pendientes,
                'respondidas':respondidas,
            })

        return data
    
    @property
    def logo(self):
        with open('static/udla/img/logo_udla.png', "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    @property
    def data(self):
        from django.forms.models import model_to_dict
        from function import mes_nombre_completo
        data = model_to_dict(self)
        hoy = getDatetime()
        pie = f"{mes_nombre_completo[hoy.strftime('%B').lower()]} - {hoy.year}"
        data['portada'] = {
            'profesor': model_to_dict(self.alumno_seccion.seccion.fk_seccion_docente_seccion.last().usuario),
            'alumno': model_to_dict(self.alumno_seccion.usuario),
            'pie': pie
        }
        actividades_padre = self.actividades_seccion.filter(actividad_padre__isnull=True).order_by('orden')
        padres = []
        for actividad_padre in actividades_padre:
            actividades_hija = self.actividades_seccion.filter(actividad_padre=actividad_padre).order_by('orden')
            hijas = []
            for actividad_hija in actividades_hija:
                actividades_nieta = self.actividades_seccion.filter(actividad_padre=actividad_hija).order_by('orden')
                nietas = []
                for actividad_nieta in actividades_nieta:
                    nieta = model_to_dict(actividad_nieta)
                    obj_nieta = ActividadRespuestaProyecto.objects.filter(proyecto=self,actividad=actividad_nieta).last()
                    if obj_nieta:
                        if actividad_nieta.tipo_entrada_id in (2,4) and 'gantt' not in actividad_nieta.nombre.lower():
                            archivos = list(eval(model_to_dict(obj_nieta).get('respuesta'))) if obj_nieta else None
                            if archivos:
                                for archivo in archivos:
                                    with open(archivo.get('ruta_archivo'), "rb") as image_file:
                                        archivo['ruta_archivo'] = base64.b64encode(image_file.read()).decode('utf-8')
                            nieta['respuesta'] = archivos
                        # elif 'gantt' in actividad_nieta.nombre.lower():
                        #     print('no implementado')
                        else:
                            nieta['respuesta'] = obj_nieta.respuesta if obj_nieta else ''
                    nietas.append(nieta)
                
                hija = model_to_dict(actividad_hija)
                obj_hija = ActividadRespuestaProyecto.objects.filter(proyecto=self,actividad=actividad_hija).last()
                if obj_hija:
                    if actividad_hija.tipo_entrada_id in (2,4) and 'gantt' not in actividad_hija.nombre.lower():
                        archivos = list(eval(model_to_dict(obj_hija).get('respuesta'))) if obj_hija else None
                        if archivos:
                            for archivo in archivos:
                                with open(archivo.get('ruta_archivo'), "rb") as image_file:
                                    archivo['ruta_archivo'] = base64.b64encode(image_file.read()).decode('utf-8')
                        hija['respuesta'] = archivos
                    else:
                        hija['respuesta'] = obj_hija.respuesta if obj_hija else ''
                    hija['actividades'] = nietas
                hijas.append(hija)

            padre = model_to_dict(actividad_padre)
            obj_padre = ActividadRespuestaProyecto.objects.filter(proyecto=self,actividad=actividad_padre).last()
            padre['respuesta'] = obj_padre.respuesta if obj_padre else ''
            padre['actividades'] = hijas
        
            padres.append(padre)

        data['actividades'] = padres

        return data
    
    @property
    def capitulos_terminados(self):
        cantidad = 0
        data = self.avance_x_captulo
        return cantidad

class ActividadRespuestaProyecto(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE,related_name='fk_proyecto_actividad_respuesta_proyecto',db_column='proyecto_id')
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE,related_name='fk_actividad_actividad_respuesta_usuario',db_column='actividad_id')
    respuesta = models.TextField(blank=False, null=False)
    ind_publicada = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, models.CASCADE, blank=False, null=False,related_name='fk_responsable_crud_actividad_respuesta_usuario',db_column='responsable_id')
    
    class Meta:
        managed = True
        db_table = 'actividad_respuesta_proyecto'
        unique_together = ('proyecto','actividad','respuesta',)

    def __str__(self):
        return f'{self.proyecto.nombre}/{self.actividad.nombre}'

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
            archivos = list(eval(self.respuesta))
            print(type(archivos))
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
    
    @property
    def hijos(self):
        return self.fk_bitacora_padre_bitacora_actividad_respuesta_proyecto.all()
    
    @property
    def timpo_desde(self):
        diferencia = getDatetime() - self.fecha
        minutos = (diferencia.seconds / 60) if diferencia.seconds > 0 else 0
        horas = (minutos / 60) if minutos > 0 else 0
        if diferencia.days == 1:
            return f'hace {int(diferencia.days)} día'
        elif diferencia.days > 1:
            return f'hace {int(diferencia.days)} días'
        elif horas == 1:
            return f'hace {int(horas)} hora'
        elif horas > 1:
            return f'hace {int(horas)} horas'
        elif minutos == 1:
            return f'hace {int(minutos)} minuto'
        elif minutos > 1:
            return f'hace {int(minutos)} minutos'
        elif diferencia.seconds == 1:
            return f'hace {int(diferencia.seconds)} segundo'
        else:
            return f'hace {int(diferencia.seconds)} segundos'


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

    
