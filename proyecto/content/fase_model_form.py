
from django import forms
from proyecto.models import Fase

class FaseModelForm(forms.ModelForm):
    nombre = forms.CharField(required=True, error_messages={'required': 'Ingrese nombre para la fase'},label='NONBRE',widget=forms.TextInput(attrs={'class':'form-control','id':'nombre','tabindex':'0'}))
    descripcion = forms.CharField(required=False, error_messages={'required': 'Ingrese la descripción de la fase'},label='DESCRIPCIÓN',widget=forms.Textarea(attrs={'class':'form-control','id':'descripcion','tabindex':'1','rows':'5'}))

    class Meta:
        model = Fase
        fields = [
            'nombre',
            'descripcion',
        ]

    def clean_nombre(self):
        return self.cleaned_data.get('nombre').strip().upper()
    
    def clean_descripcion(self):
        return self.cleaned_data.get('descripcion').strip().upper()