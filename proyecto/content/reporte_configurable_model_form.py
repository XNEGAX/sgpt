
from django import forms
from proyecto.models import ReporteConfigurable
from django_ace import AceWidget

class ReporteConfigurableModelForm(forms.ModelForm):
    nombre = forms.CharField(required=True, error_messages={'required': 'Ingrese nombre'},label='NONBRE',widget=forms.TextInput(attrs={'class':'form-control','id':'nombre','tabindex':'1','required':''}))
    codigo_fuente = forms.CharField(widget=AceWidget(
        mode="python",  # try for example "python"
        theme="twilight",  # try for example "twilight"
        wordwrap=False,
        width="100%",
        height="300px",
        minlines=None,
        maxlines=None,
        showprintmargin=True,
        showinvisibles=False,
        usesofttabs=True,
        tabsize=None,
        fontsize=None,
        toolbar=True,
        readonly=False,
        showgutter=True,  # To hide/show line numbers
        behaviours=True,  # To disable auto-append of quote when quotes are entered
    ))

    class Meta:
        model = ReporteConfigurable
        fields = [
            'nombre',
            'codigo_fuente',
        ]