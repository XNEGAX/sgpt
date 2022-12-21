
from django import forms
from django.core.exceptions import ValidationError
from proyecto.models import Seccion


class SeccionModelForm(forms.ModelForm):
    codigo = forms.CharField(required=True, error_messages={'required': 'Ingrese Código de la sección'},label='CÓDIGO',widget=forms.TextInput(attrs={'class':'form-control','id':'codigo','tabindex':'0'}))
    semestre = forms.IntegerField(required=True, error_messages={'required': 'Ingrese Semestre de la sección'},label='SEMESTRE',widget=forms.NumberInput(attrs={'class':'form-control','id':'semestre','tabindex':'1'}))
    agno = forms.IntegerField(required=True, error_messages={'required': 'Ingrese Año de la sección'},label='AÑO',widget=forms.NumberInput(attrs={'class':'form-control','id':'agno','tabindex':'2'}))

    class Meta:
        model = Seccion
        fields = [
            'codigo',
            'semestre',
            'agno',
        ]

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if codigo and Seccion.objects.filter(codigo=codigo).exists() and not self.instance:
            raise ValidationError("El código de seccón ya existe!")
        return codigo