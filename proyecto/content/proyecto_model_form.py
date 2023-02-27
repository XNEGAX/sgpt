
from django import forms
from proyecto.models import Proyecto,AlumnoSeccion

class ProyectoModelForm(forms.ModelForm):
    nombre = forms.CharField(required=True, error_messages={'required': 'Ingrese nombre para el proyecto'},label='NONBRE',widget=forms.TextInput(attrs={'class':'form-control','id':'nombre','tabindex':'1','required':''}))
    descripcion = forms.CharField(required=True, error_messages={'required': 'Ingrese una reseña para el proyecto'},label='RESEÑA',widget=forms.Textarea(attrs={'class':'form-control','id':'descripcion','tabindex':'2','rows':'5'}))
    fecha_desde = forms.DateField(required=True,error_messages={'required': 'Ingrese fecha desde'}, label='DESDE',widget=forms.DateInput(attrs={'class':'form-control','id':'fecha_desde','type':'date','tabindex':'3'}))
    fecha_hasta = forms.DateField(required=True,error_messages={'required': 'Ingrese fecha hasta'}, label='HASTA',widget=forms.DateInput(attrs={'class':'form-control','id':'fecha_hasta','type':'date','tabindex':'4'}))

    class Meta:
        model = Proyecto
        fields = [
            'nombre',
            'descripcion',
            'fecha_desde',
            'fecha_hasta',
            'alumno_seccion',
        ]

    def __init__(self, *args, **kwargs):
        super(ProyectoModelForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial',{})

        if bool(initial) and 'csrfmiddlewaretoken' in initial:
            del initial['csrfmiddlewaretoken']
        alumno_seccion_id = initial.get('alumno_seccion_id') or kwargs.get('data',{}).get('alumno_seccion_id') or self.instance.alumno_seccion_id

        if alumno_seccion_id:
            """Se generan campos default"""
            self.fields['alumno_seccion'] = forms.ModelChoiceField(
                queryset=AlumnoSeccion.objects.filter(id=alumno_seccion_id),
                label='',required=True,empty_label=None,
                widget = forms.Select(attrs={'class':'form-control','selected':alumno_seccion_id,'style':'display:none'})
            )

    def clean_alumno_seccion(self):
        return self.cleaned_data.get('alumno_seccion')

    def clean_nombre(self):
        return self.cleaned_data.get('nombre').strip().upper()
    
    def clean_descripcion(self):
        return self.cleaned_data.get('descripcion').strip().upper()

    def clean(self):
        data = self.cleaned_data
        if data.get('fecha_desde') and data.get('fecha_hasta') and (data.get('fecha_desde') > data.get('fecha_hasta')):
            self.add_error('fecha_desde', "Ingrese un rango correcto de fechas.")
        return data