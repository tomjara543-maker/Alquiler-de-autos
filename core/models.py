from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# --- CLIENTES ---
class Client(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('client-list')


# --- VEHÍCULOS ---
class Vehicle(models.Model):
    ESTADOS = [
        ('available', 'Disponible'),
        ('rented', 'Alquilado'),
    ]

    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    placa = models.CharField(max_length=20, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='available')

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"

    def get_absolute_url(self):
        return reverse('vehicle-list')


# --- ALQUILERES ---
class Rental(models.Model):
    ESTADOS = [
        ('activo', 'Activo'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="rentals")
    vehiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="rentals")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')

    def __str__(self):
        return f"Alquiler #{self.id}"

    def get_absolute_url(self):
        return reverse('rental-list')


# --- PERFIL DE USUARIO ---
class Profile(models.Model):
    ROLES = [
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES, default='empleado')

    def __str__(self):
        return f"{self.user.username} - {self.rol}"


# --- SEÑALES ---
@receiver(post_save, sender=User)
def crear_o_guardar_perfil(sender, instance, created, **kwargs):
    """Crea el perfil al crear un usuario y lo guarda al actualizarlo."""
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)
