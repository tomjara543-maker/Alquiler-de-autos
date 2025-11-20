from django.contrib import admin
from .models import Client, Vehicle, Rental


# Administración de clientes
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # Columnas visibles en la lista
    list_display = ('id', 'nombre', 'email', 'telefono')

    # Campos que se pueden buscar
    search_fields = ('nombre', 'email')


# Administración de vehículos
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    # Columnas visibles en la lista
    list_display = ('id', 'marca', 'modelo', 'placa', 'estado')

    # Campos buscables
    search_fields = ('marca', 'modelo', 'placa')

    # Filtros laterales
    list_filter = ('estado',)


# Administración de alquileres
@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    # Columnas visibles en la tabla
    list_display = ('id', 'cliente', 'vehiculo', 'fecha_inicio', 'fecha_fin', 'total')

    # Campos buscables (relaciones usando __)
    search_fields = ('cliente__nombre', 'vehiculo__placa')

    # Filtros por fecha
    list_filter = ('fecha_inicio', 'fecha_fin')
