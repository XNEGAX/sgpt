
from django import forms
from proyecto.models import Proyecto,Gantt

class GanttModelForm(forms.ModelForm):
    nombre = forms.CharField(required=True, error_messages={'required': 'Ingrese nombre de la tarea'},label='NOMBRE',widget=forms.TextInput(attrs={'class':'form-control','id':'nombre','tabindex':'0'}))
    fecha_inicio =  forms.DateField(required=True,error_messages={'required': 'Ingrese fecha incio'}, label='FECHA INICIO',widget=forms.DateInput(attrs={'class':'form-control','id':'fecha_inicio','type':'date','tabindex':'1'}))
    fecha_termino = forms.DateField(required=True,error_messages={'required': 'Ingrese fecha término'}, label='FECHA TÉRMINO',widget=forms.DateInput(attrs={'class':'form-control','id':'fecha_termino','type':'date','tabindex':''}))
    duration = forms.FloatField(required=True, error_messages={'required': 'Ingrese la duración en días'},label='DURACIÓN (Días)',widget=forms.NumberInput(attrs={'class':'form-control','id':'duration','tabindex':'3','min':1}))

    class Meta:
        model = Gantt
        fields = [
            'proyecto',
            'nombre',
            'fecha_inicio',
            'fecha_termino',
            'duration',
        ]

    def __init__(self, *args, **kwargs):
        super(GanttModelForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial','')
        proyecto_id = initial.get('proyecto_id')
        if proyecto_id:
            self.fields['proyecto'] = forms.ModelChoiceField(
                queryset=Proyecto.objects.filter(id=proyecto_id),
                label='',required=True,empty_label=None,
                widget = forms.Select(attrs={'class':'form-control','selected':proyecto_id,'style':'display:none'})
            )

    def clean_nombre(self):
        return self.cleaned_data.get('nombre').strip().upper()
    
    def clean_descripcion(self):
        return self.cleaned_data.get('descripcion').strip().upper()
    
    def clean(self):
        data = self.cleaned_data
        if data.get('fecha_inicio') and data.get('fecha_termino') and (data.get('fecha_inicio') > data.get('fecha_termino')):
            self.add_error('fecha_inicio', "Ingrese un rango correcto de fechas.")
        if data.get('fecha_inicio') and (data.get('fecha_inicio')<data.get('proyecto').fecha_desde.date()):
            self.add_error('fecha_inicio', "La fecha de inicio es menor a la fecha de inicio del proyecto")
        if data.get('fecha_termino') and (data.get('fecha_termino')<data.get('proyecto').fecha_hasta.date()):
            self.add_error('fecha_termino', "La fecha término es mayor a la fecha de término del proyecto")
        return data

   