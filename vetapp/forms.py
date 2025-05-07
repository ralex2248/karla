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
            'anamnesis_remota', 'cc', 'anamnesis_actual', 'pc', 'tllc', 'oidos', 
            'ojos', 'boca', 'linfonodo_submandibular', 'rt', 'fc', 'fr', 
            'pulso_femoral', 'palpacion_abdominal', 'miembro_reproductor', 
            'linfonodo_inguinal', 'pelaje', 'temperatura', 'tratamiento', 
            'recomendaciones', 'receta', 'fecha_visita'
        ]
        widgets = {
            'fecha_visita': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(FichaForm, self).__init__(*args, **kwargs)
        
        # Si el objeto ya existe (es una edición), permite modificar la fecha
        if self.instance.pk:
            # El campo 'fecha_visita' estará disponible para edición solo si el objeto existe
            self.fields['fecha_visita'].required = False  # La hace no obligatoria al editar
        else:
            # Al crear el objeto, fecha_visita no será editable
            self.fields['fecha_visita'].widget.attrs['readonly'] = 'readonly'
            self.fields['fecha_visita'].initial = 'fecha actual'  # Si lo deseas, puedes agregar la fecha actual como valor predeterminado al crear el objeto

        # Para completar automáticamente el dueño al seleccionar una mascota
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
