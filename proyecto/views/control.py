from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.shortcuts import render
from proyecto.auth import RoyalGuard
from proyecto.auth import set_aditional_paramas
from django.views.generic import View
from django.views.generic import ListView
from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django.db.models.functions import Lower
from django.contrib.auth import login
from django.forms.models import model_to_dict
import json
# models
from proyecto.models import Parametro
from proyecto.models import PerfilUsuarioActivo
from proyecto.models import PerfilUsuario
from django.contrib.auth.models import User
from proyecto.models.log import Log
from django.contrib.contenttypes.models import ContentType

class Salir(LogoutView):
    def get(self, request, *args, **kwargs):
        rediredct_login = f'/users/login/?next=/'
        return redirect(rediredct_login)

class CambioPerfil(RoyalGuard,View):
    def get(self, request):
        perfil_invitado = Parametro.objects.filter(nombre='perfil_invitado').values('metadatos').last()['metadatos']['perfil_id']
        perfil_activo = PerfilUsuarioActivo.objects.get(usuario=request.user).perfil_id
        perfiles_disponibles = PerfilUsuario.objects.filter(usuario=request.user).values(
            'perfil_id','perfil__nombre'
        ).exclude(
            perfil_id__in=[perfil_invitado,perfil_activo]
        ).annotate(url_logo_perfil=Lower( Concat(Value('/static/udla/img/'),'perfil__nombre',Value('.png'),output_field=CharField())) ).distinct()
        context = {
            'perfil_activo':perfil_activo,
            'perfiles_disponibles':perfiles_disponibles
        }
        return render(request, 'control/content_cambio_perfil.html',context)

    def post(self,request):
        perfil = request.POST.get('perfil')
        PerfilUsuarioActivo.objects.filter(usuario=request.user).update(perfil_id=perfil)
        set_aditional_paramas(request.user,request)
        return redirect('proyecto:home')


class Error403(View):
    def get(self, request):
        return render(request, 'control/errores.html',context={'estado':403},status=403)


class ImpersonarUsuario(RoyalGuard,View):
    def post(self, request):
        impersonate = User.objects.get(id=request.POST.get('usuario_id'))
        login(request, impersonate)
        set_aditional_paramas(impersonate,request)
        return redirect('proyecto:home')
    


class Auditoria(ListView):
    template_name = 'admin/auditoria/index.html'
    paginate_by = 10
    model = Log
    excluir = [
        'logentry',
        'permission',
        'group',
        'user',
        'contenttype',
        'session',
        'site',
        'microsoftaccount',
        'xboxliveaccount',
        'perfil',
        'perfilmodulo',
        'modulo',
        'parametro',
        'tipoentrada',
        'log',
        'semestre',
        'perfilusuarioactivo'
    ]

    def get_context_data(self, **kwargs):
        from django.core import serializers
        context = super(Auditoria, self).get_context_data(**kwargs)
        lista_modelos = ContentType.objects.exclude(model__in=self.excluir).distinct().order_by('model')

        data_combo_modelo = []
        for modelo in lista_modelos:
            data_combo_modelo.append({
                'id':modelo.id,
                'tabla':modelo.model_class()._meta.db_table
            })
        context['data_combo_modelo'] = data_combo_modelo
        context['model_selected'] = int(self.request.GET.get('modelo')) if self.request.GET.get('modelo') else ContentType.objects.all().distinct().order_by('model').first().id

        fields = ['accion']
        for f in ContentType.objects.get(pk=context.get('model_selected')).model_class()._meta.get_fields():
            if 'fk' not in f.name and f.name != 'id':
                fields.append(f.name)
        context['fields'] = fields
        
        
        logs = context.get('object_list')
        data_logs = []
        for log in logs:
            metadatos = model_to_dict(log).get('metadatos')
            detalle = json.loads(metadatos).get('detalle')
            temp = json.loads(detalle)[0].get('fields')
            if temp.get('usuario'):
                temp['usuario'] = User.objects.get(pk=temp.get('usuario')).get_full_name()
            temp.update({
                'accion':log.accion_nombre,
                'fecha':log.fecha.strftime('%Y-%m-%d %H:%M'),
                'responsable':log.responsable.get_full_name()
            })
            data_logs.append(temp)

        context['object_list'] = data_logs
        return context

    def get_queryset(self):
        model_selected= ContentType.objects.all().distinct().order_by('model').first()
        if self.request.GET.get('modelo'):
            model_selected = int(self.request.GET.get('modelo'))
        logs = Log.objects.filter(modelo_id=model_selected)
        return logs
