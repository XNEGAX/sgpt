
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from proyecto.models import Seccion,Semestre

class SeccionModelForm(forms.ModelForm):
    codigo = forms.CharField(required=True, error_messages={'required': 'Ingrese Código de la sección'},label='CÓDIGO',widget=forms.TextInput(attrs={'class':'form-control','id':'codigo','tabindex':'0'}))
    semestre = forms.ModelChoiceField(queryset=Semestre.objects.all().order_by('id'),required=True, error_messages={'required': 'seleccione el semestre'},label='SEMESTRE',widget=forms.Select(attrs={'class':'form-control','id':'semestre','tabindex':'1'}))
    fecha_desde = forms.DateField(required=True,error_messages={'required': 'Ingrese fecha desde'}, label='DESDE',widget=forms.DateInput(attrs={'class':'form-control','id':'fecha_desde','type':'date','tabindex':'3'}))
    fecha_hasta = forms.DateField(required=True,error_messages={'required': 'Ingrese fecha hasta'}, label='HASTA',widget=forms.DateInput(attrs={'class':'form-control','id':'fecha_hasta','type':'date','tabindex':'4'}))

    class Meta:
        model = Seccion
        fields = [
            'codigo',
            'semestre',
            'fecha_desde',
            'fecha_hasta',
        ]

    def clean_codigo(self):
        return self.cleaned_data.get('codigo').strip().upper()

    def clean(self):
        data = self.cleaned_data
        if data.get('fecha_desde') > data.get('fecha_hasta'):
            self.add_error('fecha_desde', "Ingrese un rango correcto de fechas.")
        return data