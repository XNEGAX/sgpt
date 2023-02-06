
from django import forms
from django.db.models import Max
from proyecto.models import Actividad,Fase,TipoEntrada

class ActividadModelForm(forms.ModelForm):
    nombre = forms.CharField(required=True, error_messages={'required': 'Ingrese nombre para la actividad'},label='NONBRE',widget=forms.TextInput(attrs={'class':'form-control','id':'nombre','tabindex':'0'}))
    descripcion = forms.CharField(required=True, error_messages={'required': 'Ingrese la descripción de la actividad'},label='DESCRIPCIÓN',widget=forms.Textarea(attrs={'class':'form-control','id':'descripcion','tabindex':'1','rows':'5'}))
    fase = forms.ModelChoiceField(queryset=Fase.objects.all().order_by('nombre'),required=False,label='FASE',widget=forms.Select(attrs={'class':'form-control','id':'fase','tabindex':'2'}))
    tipo_entrada = forms.ModelChoiceField(queryset=TipoEntrada.objects.all().order_by('nombre'),required=True,label='TIPO ENTRADA',widget=forms.Select(attrs={'class':'form-control','id':'tipo_entrada','tabindex':'3'}))
    orden = forms.IntegerField(required=True, error_messages={'required': 'Ingrese la posición de la actividad'},label='POSICIÓN',widget=forms.TextInput(attrs={'class':'form-control','id':'orden','tabindex':'4'}))

    class Meta:
        model = Actividad
        fields = [
            'nombre',
            'descripcion',
        ]

    def clean_nombre(self):
        return self.cleaned_data.get('nombre').strip().upper()
    
    def clean_descripcion(self):
        return self.cleaned_data.get('descripcion').strip().upper()

    def clean(self):
        data = self.cleaned_data
        print("data.get('orden')")
        print(data.get('orden'))
        previus_order_fase = Actividad.objects.filter(seccion=data.get('seccion'),orden=data.get('orden')).last()
        if previus_order_fase:
            print('previus_order_fase')
            print(previus_order_fase)
            
            previus_order_fase.orden = Fase.objects.aggregate(Max('orden'))
            print('previus_order_fase.orden')
            print(previus_order_fase.orden)
            # previus_order_fase.save()
        return data