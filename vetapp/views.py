from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ClienteForm, MascotaForm, FichaForm
from .models import Cliente, Mascota, Ficha
from io import BytesIO
import base64
import matplotlib.pyplot as plt


# Vista de inicio
@login_required
def home(request):
    fichas = Ficha.objects.all().order_by('-id_ficha')[:10]
    return render(request, 'vetapp/home.html', {'fichas': fichas})

# Vista para agregar cliente
@login_required
def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClienteForm()
    return render(request, 'vetapp/agregar_cliente.html', {'form': form})

# Vista para agregar mascota
@login_required
def agregar_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MascotaForm()
    return render(request, 'vetapp/agregar_mascota.html', {'form': form})

# Vista para agregar ficha
@login_required
def agregar_ficha(request):
    if request.method == 'POST':
        form = FichaForm(request.POST)
        if form.is_valid():
            ficha = form.save(commit=False)
            ficha.cliente = ficha.mascota.cliente  # Asocia el cliente desde la mascota
            ficha.save()
            return redirect('home')
    else:
        form = FichaForm()
    return render(request, 'vetapp/agregar_ficha.html', {'form': form})

# Vista para ver los clientes
@login_required
def ver_cliente(request):
    clientes = Cliente.objects.all()
    return render(request, 'vetapp/ver_cliente.html', {'clientes': clientes})


# Vista para ver las mascotas
@login_required
def ver_mascota(request):
    mascotas = Mascota.objects.all()
    return render(request, 'vetapp/ver_mascotas.html', {'mascotas': mascotas})

# Vista para ver las fichas
@login_required
def ver_ficha(request):
    fichas = Ficha.objects.all()
    return render(request, 'vetapp/ver_ficha.html', {'fichas': fichas})

# Vista para obtener cliente por mascota (modificada para responder con JSON)
def obtener_cliente_por_mascota(request):
    if request.method == 'GET':  # Cambié a GET para trabajar con AJAX
        mascota_id = request.GET.get('mascota_id')  # Usamos GET en lugar de POST para las peticiones AJAX
        if mascota_id:
            try:
                # Cambié a 'id_mascota' en la consulta, ya que esa es la clave primaria en el modelo Mascota
                mascota = Mascota.objects.get(id_mascota=mascota_id)
                cliente = mascota.cliente
                # Ahora se accede a 'id_cliente' en lugar de 'id'
                return JsonResponse({'cliente_id': cliente.id_cliente, 'cliente_nombre': cliente.nombre})
            except Mascota.DoesNotExist:
                return JsonResponse({'error': 'Mascota no encontrada'}, status=400)
        return JsonResponse({'error': 'ID de mascota no proporcionado'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Vista para las últimas 10 fichas
def ultimas_10_fichas(request):
    fichas = Ficha.objects.all().order_by('-fecha_visita')[:10]
    return render(request, 'vetapp/ultimas_fichas.html', {'fichas': fichas})

# Vista para ver el detalle de una ficha
def ver_detalle_ficha(request, id_ficha):
    ficha = Ficha.objects.get(id_ficha=id_ficha)
    return render(request, 'vetapp/detalle_ficha.html', {'ficha': ficha})

# Nueva vista para ver las fichas asociadas a una mascota
@login_required
def ver_fichas_mascota(request, id_mascota):
    # Obtener la mascota por ID
    mascota = get_object_or_404(Mascota, id_mascota=id_mascota)
    
    # Obtener el cliente asociado a la mascota
    cliente = mascota.cliente

    # Obtener todas las fichas asociadas a la mascota
    fichas = Ficha.objects.filter(mascota=mascota)

    # Renderizar el template con los datos
    return render(request, 'vetapp/info-masc.html', {
        'mascota': mascota,
        'cliente': cliente,
        'fichas': fichas
    })

def editar_mascota(request, id_mascota):
    mascota = get_object_or_404(Mascota, id_mascota=id_mascota)
    
    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('ver_mascotas')
    else:
        form = MascotaForm(instance=mascota)
    
    return render(request, 'vetapp/editar_mascota.html', {'form': form})

def editar_cliente(request, id_cliente):
    # Obtener el cliente a editar
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)

    # Verifica si el formulario fue enviado
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()  # Guarda los cambios
            return redirect('ver_cliente')  # Redirige al listado de clientes después de la actualización
    else:
        # Si es un GET, pre-cargar los datos en el formulario
        form = ClienteForm(instance=cliente)

    # Renderiza la plantilla y pasa el formulario
    return render(request, 'vetapp/editar_cliente.html', {'form': form, 'cliente': cliente})

def editar_ficha(request, id_ficha):
    ficha = get_object_or_404(Ficha, id_ficha=id_ficha)  # Obtenemos la ficha a editar
    
    if request.method == 'POST':
        form = FichaForm(request.POST, instance=ficha)
        if form.is_valid():
            form.save()
            return redirect('ver_fichas')  # Redirige al listado de fichas después de guardar
    else:
        form = FichaForm(instance=ficha)  # Cargamos los datos de la ficha en el formulario
    
    return render(request, 'vetapp/editar_ficha.html', {'form': form, 'ficha': ficha})


def graficos(request):
    # Contar las mascotas por especie
    canino_count = Mascota.objects.filter(especie='Canino').count()
    felino_count = Mascota.objects.filter(especie='Felino').count()
    otro_count = Mascota.objects.filter(especie='Otro').count()

    # Contar los clientes por región
    region_a_count = Cliente.objects.filter(direccion__contains="Región A").count()
    region_b_count = Cliente.objects.filter(direccion__contains="Región B").count()
    region_c_count = Cliente.objects.filter(direccion__contains="Región C").count()

    # Crear gráficos
    # 1. Gráfico de barras: Mascotas por especie
    fig, ax = plt.subplots()
    ax.bar(['Canino', 'Felino', 'Otro'], [canino_count, felino_count, otro_count], color=['blue', 'green', 'red'])
    ax.set_title('Mascotas por Especie')
    ax.set_xlabel('Especie')
    ax.set_ylabel('Cantidad')

    # Guardar el gráfico en una imagen en memoria
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    mascota_chart = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    # 2. Gráfico de barras: Clientes por región
    fig, ax = plt.subplots()
    ax.bar(['Región A', 'Región B', 'Región C'], [region_a_count, region_b_count, region_c_count], color=['purple', 'orange', 'cyan'])
    ax.set_title('Clientes por Región')
    ax.set_xlabel('Región')
    ax.set_ylabel('Cantidad')

    # Guardar el gráfico en una imagen en memoria
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    region_chart = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    # Contexto para el template
    context = {
        'canino_count': canino_count,
        'felino_count': felino_count,
        'otro_count': otro_count,
        'region_a_count': region_a_count,
        'region_b_count': region_b_count,
        'region_c_count': region_c_count,
        'mascota_chart': mascota_chart,
        'region_chart': region_chart,
    }

    return render(request, 'vetapp/graficos.html', context)