from django.db import models
from datetime import date

# Modelo de Usuario Personalizado
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    celular = models.CharField(max_length=15)
    correo = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

# Modelo Cliente
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=20)
    mascota = models.CharField(max_length=100)  # Solo como dato de referencia rápida
    correo = models.EmailField()
    direccion = models.CharField(max_length=200)
    rut = models.CharField(max_length=12)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Modelo Mascota
class Mascota(models.Model):
    SEXO_CHOICES = [
        ('Macho', 'Macho'),
        ('Hembra', 'Hembra'),
    ]

    ESPECIE_CHOICES = [
        ('Canino', 'Canino'),
        ('Felino', 'Felino'),
        ('Otro', 'Otro'),
    ]

    ESTADO_REPRODUCTIVO_CHOICES = [
        ('Entero', 'Entero'),
        ('Esterilizado', 'Esterilizado'),
    ]

    id_mascota = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mascotas')
    nombre = models.CharField(max_length=100)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    raza = models.CharField(max_length=100)
    especie = models.CharField(max_length=20, choices=ESPECIE_CHOICES)
    fecha_nacimiento = models.DateField()
    estado_reproductivo = models.CharField(max_length=15, choices=ESTADO_REPRODUCTIVO_CHOICES)

    def calcular_edad_completa(self):
        today = date.today()
        dias_totales = (today - self.fecha_nacimiento).days
        años = dias_totales // 365
        dias = dias_totales % 365

        años_texto = f"{años} año" if años == 1 else f"{años} años"
        dias_texto = f"{dias} día" if dias == 1 else f"{dias} días"

        return f"{años_texto} y {dias_texto}"

    edad = property(calcular_edad_completa)

    def __str__(self):
        return f"{self.nombre} ({self.especie})"

# Modelo Ficha
class Ficha(models.Model):
    id_ficha = models.AutoField(primary_key=True)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='fichas')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_visita = models.DateField(auto_now_add=True)
    motivo_consulta = models.TextField()
    anamnesis_remota = models.TextField()
    anamnesis_actual = models.TextField()
    pc = models.TextField()
    tllc = models.TextField()
    oidos = models.TextField()
    ojos = models.TextField()
    boca = models.TextField()
    linfonodo_submandibular = models.TextField()
    rt = models.CharField(max_length=10)
    fc = models.CharField(max_length=10)
    fr = models.CharField(max_length=10)
    pulso_femoral = models.TextField()
    palpacion_abdominal = models.TextField()
    miembro_reproductor = models.TextField()
    linfonodo_inguinal = models.TextField()
    pelaje = models.TextField()
    temperatura = models.CharField(max_length=10)
    tratamiento = models.TextField()
    recomendaciones = models.TextField()
    receta = models.TextField()

    def __str__(self):
        return f"Ficha {self.id_ficha} - {self.mascota.nombre}"
