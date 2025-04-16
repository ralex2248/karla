from django import forms
from .models import Cliente, Mascota, Ficha
from django.http import JsonResponse

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

    # Para completar automáticamente el dueño al seleccionar una mascota
    def __init__(self, *args, **kwargs):
        super(MascotaForm, self).__init__(*args, **kwargs)
        if 'cliente' in self.fields:
            self.fields['cliente'].widget.attrs.update({'class': 'cliente-select', 'readonly': 'readonly'})

class FichaForm(forms.ModelForm):
    class Meta:
        model = Ficha
        fields = [
            'mascota', 'cliente', 'motivo_consulta', 
            'anamnesis_remota', 'anamnesis_actual', 'pc', 'tllc', 'oidos', 
            'ojos', 'boca', 'linfonodo_submandibular', 'rt', 'fc', 'fr', 
            'pulso_femoral', 'palpacion_abdominal', 'miembro_reproductor', 
            'linfonodo_inguinal', 'pelaje', 'temperatura', 'tratamiento', 
            'recomendaciones', 'receta'
        ]
        widgets = {
            'fecha_visita': forms.DateInput(attrs={'type': 'date'}),
        }

    # Para completar automáticamente el dueño al seleccionar una mascota
    def __init__(self, *args, **kwargs):
        super(FichaForm, self).__init__(*args, **kwargs)
        if 'cliente' in self.fields:
            self.fields['cliente'].widget.attrs.update({'class': 'cliente-select', 'readonly': 'readonly'})

# Vista para obtener el cliente a partir de la mascota
def obtener_cliente_por_mascota(request):
    mascota_id = request.GET.get('mascota_id')
    try:
        mascota = Mascota.objects.get(id=mascota_id)
        cliente = mascota.cliente
        return JsonResponse({
            'cliente_id': cliente.id,
            'cliente_nombre': str(cliente)
        })
    except Mascota.DoesNotExist:
        return JsonResponse({'error': 'Mascota no encontrada'}, status=404)
