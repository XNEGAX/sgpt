from django import forms
from django.contrib.auth.models import User

class ProveedorForm(forms.ModelForm):
    prr_rut = forms.IntegerField(required=True,label='Rut',widget=forms.TextInput(attrs={'class': 'form-control','id':'prr_rut'}))
    prr_razon_social = forms.CharField(required=True, error_messages={'required': 'Ingrese la razon social'},label='Razón social',widget=forms.TextInput(attrs={'class':'form-control','id':'prr_razon_social'}))
    ncn = forms.ModelChoiceField(required=True,error_messages={'required': 'Seleccione Nacionalidad'}, label='Nacionalidad',queryset=Nacionalidad.objects.filter(ncn_vigencia=True).order_by('ncn_nombre'),empty_label="Seleccione una opción",widget=forms.Select(attrs={'class':'full-width select2-hidden-accessible','data-init-plugin':'select2','tabindex':'-1','aria-hidden':'true','id':'cmb_nacionalidad'}))
    gic = forms.ModelChoiceField(required=True,error_messages={'required': 'Seleccione giro comercial'}, label='Giro comercial',queryset=GiroComercial.objects.filter(gic_vigencia=True).order_by('gic_descripcion'),empty_label="Seleccione una opción",widget=forms.Select(attrs={'class':'full-width select2-hidden-accessible','data-init-plugin':'select2','tabindex':'-1','aria-hidden':'true','id':'cmb_giro_comercial'}))
    prr_nombre_fantasia = forms.CharField(required=True, error_messages={'required': 'Ingrese el nombre de fantasia'},label='Nombre de fantasia',widget=forms.TextInput(attrs={'class':'form-control','id':'prr_nombre_fantasia'}))
    prr_observacion = forms.CharField(required=True, error_messages={'required': 'Ingrese la observacion'},label='Observación <a style="color: #ffc107;">(Opcional)</a>',widget=forms.Textarea(attrs={'class':'form-control','id':'prr_observacion'}))
    bnc = forms.ModelChoiceField(required=False,label='Banco <a style="color: #ffc107;">(Opcional)</a>',queryset=Banco.objects.filter(bnc_vigencia=True).order_by('bnc_nombre'),empty_label="Seleccione una opción",widget=forms.Select(attrs={'class':'full-width select2-hidden-accessible','data-init-plugin':'select2','tabindex':'-1','aria-hidden':'true','id':'cmb_banco'}))
    prr_numero_cuenta = forms.IntegerField(required=False,label='Numero de cuenta',widget=forms.TextInput(attrs={'class': 'form-control','id':'prr_numero_cuenta', 'disabled':'disabled'}))
    t_tcb = forms.ModelChoiceField(required=False,label='Tipo de cuenta',queryset=TipoCuentaBanco.objects.filter(t_tcb_vigencia=True).order_by('t_tcb_descripcion'),empty_label="Seleccione una opción",widget=forms.Select(attrs={'data-init-plugin':'select2','tabindex':'-1','aria-hidden':'true','id':'cmb_tipo_cuenta', 'disabled':'disabled'}))
    prr_dv = forms.CharField(required=True, error_messages={'required': 'Ingrese el dv'},label='Dv',widget=forms.TextInput(attrs={'class':'form-control','id':'prr_dv'}))
    
    class Meta:
        model = User
        fields = ['prr_rut','prr_razon_social','ncn','gic','prr_nombre_fantasia','prr_observacion','bnc','prr_numero_cuenta','t_tcb','prr_dv']

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs) 