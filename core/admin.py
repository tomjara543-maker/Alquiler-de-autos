from django.contrib import admin
from .models import Client, Vehicle, Rental

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'telefono')
    search_fields = ('nombre', 'email')


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'marca', 'modelo', 'placa', 'estado')
    search_fields = ('marca', 'modelo', 'placa')
    list_filter = ('estado',)


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'vehiculo', 'fecha_inicio', 'fecha_fin', 'total')
    search_fields = ('cliente__nombre', 'vehiculo__placa')
    list_filter = ('fecha_inicio', 'fecha_fin')
