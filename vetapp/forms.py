from django import forms
from .models import Cliente, Mascota, Ficha

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'fecha-campo'
            }),
        }

class FichaForm(forms.ModelForm):
    class Meta:
        model = Ficha
        fields = '__all__'
