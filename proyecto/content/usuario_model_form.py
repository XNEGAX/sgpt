
from django import forms
from django.core.exceptions import ValidationError
from function import validar_rut
from django.contrib.auth.models import User
from proyecto.models import PerfilUsuario
from proyecto.models import PerfilUsuarioActivo


class UsuarioModelForm(forms.ModelForm):
    username = forms.CharField(required=True, error_messages={'required': 'Ingrese Rut del usuario'},label='RUT',widget=forms.TextInput(attrs={'class':'form-control','id':'username','tabindex':'0'}))
    first_name = forms.CharField(required=True,error_messages={'required': 'Ingrese Nombre del usuario'},label='NOMBRE',widget=forms.TextInput(attrs={'class':'form-control','id':'first_name','tabindex':'1'}))
    last_name= forms.CharField(required=True,error_messages={'required': 'Ingrese Apellidos del usuario'},label='APELLIDOS',widget=forms.TextInput(attrs={'class':'form-control','id':'last_name','tabindex':'2'}))
    email = forms.EmailField(required=True,error_messages={'required': 'Ingrese Email institucional del usuario'},label='Email Institucional',widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Ej: usuario@edu.udla.cl','id':'email','tabindex':'3'}))
        
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


    def __init__(self, *args, **kwargs):
        super(UsuarioModelForm, self).__init__(*args, **kwargs)
        data = kwargs.get('data')
        if data and data.get('perfiles[]'):
            perfiles = list(data.get('perfiles[]'))
            while("," in perfiles):
                perfiles.remove(",")
            self.perfiles = perfiles
        if data and data.get('responsable'):
            self.responsable = data.get('responsable')

    def save(self, *args, **kwargs):
        usuario = super(UsuarioModelForm, self).save(*args, **kwargs)
        usuario.is_staff =True
        usuario.save()
        PerfilUsuario.objects.filter(usuario=usuario).delete()
        for perfil in self.perfiles:
            if not PerfilUsuario.objects.filter(perfil_id=perfil,usuario=usuario).exists():
                PerfilUsuario.objects.create(
                    perfil_id=perfil,
                    usuario=usuario,
                    responsable=self.responsable
                )
        PerfilUsuarioActivo.objects.filter(usuario=usuario).delete()
        if self.perfiles:
            PerfilUsuarioActivo.objects.create(
                perfil_id=self.perfiles[0],
                usuario=usuario,
                responsable=self.responsable
            )
        return usuario

    def clean_username(self):
        rut = self.cleaned_data['username']
        if not validar_rut.is_valid_rut(rut):
            raise ValidationError("El rut ingresado no es válido!")
        username = f"{rut.replace('.','').replace('-','')}@ACADEMICOS.uamericas.cl"
        if User.objects.filter(username=username).exists() and not self.instance:
            raise ValidationError("El rut ingresado ya existe!")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name != '' and first_name is not None:
            first_name = first_name.strip().upper()
        else:
            raise ValidationError("El nombre no puede estar vacío!")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if last_name != '' and last_name is not None:
            last_name = last_name.strip().upper()
        else:
            raise ValidationError("Los apellidos no pueden estar vacío!")
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if '@edu.udla.cl' not in email.lower():
            raise ValidationError("Debe ingresar el correo institucional!")
        return email