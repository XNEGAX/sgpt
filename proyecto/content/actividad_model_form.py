
from django import forms
from collections import OrderedDict
from django.db.models import Q
from django.db.models import Max,Min
from proyecto.models import Actividad,TipoEntrada,Seccion

TIPO_ACTIVIDAD = [
    (1, 'Ninguno'),
    (2, 'Otra actividad'),
]

class ActividadModelForm(forms.ModelForm):
    tipo_actividad = forms.ChoiceField(required=False,label='REQUIERE DE',widget=forms.RadioSelect,choices=TIPO_ACTIVIDAD, )

    class Meta:
        model = Actividad
        fields = [
            'seccion',
            'actividad_padre',
            'nombre',
            'descripcion',
            'tipo_entrada',
            'orden',
        ]

    def __init__(self, *args, **kwargs):
        super(ActividadModelForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial','')

        if bool(initial) and 'csrfmiddlewaretoken' in initial:
            del initial['csrfmiddlewaretoken']
        seccion_id = initial.get('seccion_id')
        if seccion_id:
            """Se inicializan los radio"""
            tipo_actividad = int(initial.get('tipo_actividad')) if initial.get('tipo_actividad') else 1
            if self.data and self.data.get('tipo_actividad'):
                tipo_actividad = self.data.get('tipo_actividad')
            if self.instance and self.instance.pk and not initial.get('tipo_actividad') and (not self.data and not self.data.get('tipo_actividad')):
                if self.instance.actividad_padre:
                    tipo_actividad = 2
                else:
                    tipo_actividad = 1
            self.fields['tipo_actividad'].initial = tipo_actividad
            """se toman desiciones en base a los radio"""

            fields_keyOrder = ['tipo_actividad','actividad_padre','nombre','descripcion','tipo_entrada','orden']
            if tipo_actividad== 2:
                actividades =[]
                for actividad in Actividad.objects.filter(seccion_id=seccion_id,actividad_padre__actividad_padre_id__isnull=True,ind_base=False).order_by('orden'):
                    actividades.append((actividad.id,f"{actividad.orden_formateado} {actividad.nombre}"))

                self.fields['actividad_padre'] = forms.ChoiceField(
                    choices=tuple(sorted(actividades, key=lambda x: x[1])),
                    label='ACTIVIDAD PADRE',required=True,
                    widget=forms.Select(attrs={'class':'form-control','id':'tipo_entrada','tabindex':'0'})
                )
                fields_keyOrder  = ['tipo_actividad','actividad_padre','nombre','descripcion','tipo_entrada','orden']
            
            else:
                if not self.is_bound:
                    fields_keyOrder = ['tipo_actividad','nombre','descripcion','tipo_entrada','orden']

            self.fields = OrderedDict((k, self.fields[k]) for k in fields_keyOrder)
            """Se generan campos default"""
            self.fields['seccion'] = forms.ModelChoiceField(
                queryset=Seccion.objects.filter(id=seccion_id),
                label='',required=True,empty_label=None,
                widget = forms.Select(attrs={'class':'form-control','selected':seccion_id,'style':'display:none'})
            )
            self.fields['nombre'] = forms.CharField(required=True, error_messages={'required': 'Ingrese nombre para la actividad'},label='NONBRE',widget=forms.TextInput(attrs={'class':'form-control','id':'nombre','tabindex':'1','required':''}))
            self.fields['descripcion'] = forms.CharField(required=False, error_messages={'required': 'Ingrese la descripción de la actividad'},label='DESCRIPCIÓN',widget=forms.Textarea(attrs={'class':'form-control','id':'descripcion','tabindex':'2','rows':'5'}))
            self.fields['tipo_entrada'] = forms.ModelChoiceField(queryset=TipoEntrada.objects.all().order_by('nombre'),required=False, error_messages={'required': 'Ingrese el tipo de dato para la respuesta'},label='TIPO DE DATO ESPERADO',widget=forms.Select(attrs={'class':'form-control','id':'tipo_entrada','tabindex':'4'}))
            self.fields['orden'] = forms.FloatField(required=True, error_messages={'required': 'Ingrese la posición de la actividad'},label='POSICIÓN',widget=forms.NumberInput(attrs={'class':'form-control','id':'orden','tabindex':'5','min':0,'min':1}))


    def clean_nombre(self):
        return self.cleaned_data.get('nombre').strip().upper()
    
    def clean_descripcion(self):
        return self.cleaned_data.get('descripcion').strip().upper()

    def clean(self):
        data = self.cleaned_data
        previus_order_actividad = Actividad.objects.filter(seccion=data.get('seccion'),orden=data.get('orden'),actividad_padre=data.get('actividad_padre')).last()
        if previus_order_actividad:
            actividades = Actividad.objects.filter(seccion=data.get('seccion'),actividad_padre=data.get('actividad_padre'))
            now_min = actividades.aggregate(Min('orden')).get('orden__min')
            now_max = actividades.aggregate(Max('orden')).get('orden__max')+1
            for now in range(now_min,now_max):
                if not actividades.filter(orden=now).exists():
                    previus_order_actividad.orden = now
                    previus_order_actividad.save()
                    return data
                elif now == self.instance.orden:
                    previus_order_actividad.orden = now
                    previus_order_actividad.save()
                    return data

            previus_order_actividad.orden = now_max
            previus_order_actividad.save()
        return data
            