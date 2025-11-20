from django.db import models
from django.urls import reverse
        # Para obtener URLs automáticamente

from django.contrib.auth.models import User
        # Modelo de usuarios de Django

from django.db.models.signals import post_save
        # Señal que se ejecuta cuando un usuario es creado o guardado

from django.dispatch import receiver
        # Decorador para conectar señales


#  CLIENTES
class Client(models.Model):
    # Datos básicos del cliente
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)     # No se puede repetir
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        # Redirección automática al listado después de crear/editar
        return reverse('client-list')


# VEHÍCULOS
class Vehicle(models.Model):
    # Opciones del estado del vehículo
    ESTADOS = [
        ('available', 'Disponible'),
        ('rented', 'Alquilado'),
    ]

    # Información del vehículo
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    placa = models.CharField(max_length=20, unique=True)   # No duplicada
    estado = models.CharField(max_length=20, choices=ESTADOS, default='available')

    def __str__(self):
        # Cómo se verá en el admin y listas
        return f"{self.marca} {self.modelo} ({self.placa})"

    def get_absolute_url(self):
        return reverse('vehicle-list')


# ALQUILERES 
class Rental(models.Model):
    # Estados del alquiler
    ESTADOS = [
        ('activo', 'Activo'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]

    # Relación con cliente y vehículo
    cliente = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="rentals")
    vehiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="rentals")

    # Fechas del alquiler
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    # Total generado por el alquiler
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Estado del alquiler
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')

    def __str__(self):
        return f"Alquiler #{self.id}"

    def get_absolute_url(self):
        return reverse('rental-list')


# PERFIL DE USUARIO
class Profile(models.Model):
    # Roles disponibles dentro del sistema
    ROLES = [
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
    ]

    # Relación 1 a 1 con User
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Rol del usuario
    rol = models.CharField(max_length=20, choices=ROLES, default='empleado')

    def __str__(self):
        return f"{self.user.username} - {self.rol}"


# SEÑALES 
@receiver(post_save, sender=User)
def crear_o_guardar_perfil(sender, instance, created, **kwargs):
    """Crea el perfil al crear un usuario y lo guarda al actualizarlo."""
    if created:
        Profile.objects.create(user=instance)
    else:
        # Si el perfil existe lo guarda, si no existe lo crea
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)
