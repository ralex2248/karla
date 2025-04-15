from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ClienteForm, MascotaForm, FichaForm
from .models import Cliente, Mascota

@login_required
def home(request):
    return render(request, 'vetapp/home.html')

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

@login_required
def agregar_ficha(request):
    if request.method == 'POST':
        form = FichaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FichaForm()
    return render(request, 'vetapp/agregar_ficha.html', {'form': form})

@login_required
def ver_cliente(request):
    clientes = Cliente.objects.all()
    return render(request, 'vetapp/ver_cliente.html', {'clientes': clientes})

def ver_mascota(request):
    mascotas = Mascota.objects.all()
    return render(request, 'vetapp/ver_mascotas.html', {'mascotas': mascotas})