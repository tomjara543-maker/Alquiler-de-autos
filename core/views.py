from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db import models
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .forms import RegisterForm, ClientForm, VehicleForm, RentalForm
from .models import Client, Vehicle, Rental


class AdminRequiredMixin(UserPassesTestMixin):
    # Permite acceso solo a superusuarios
    def test_func(self):
        return self.request.user.is_superuser

    # Si el usuario no tiene permiso, lo devuelve al dashboard
    def handle_no_permission(self):
        return redirect('dashboard')


def register(request):
    # Formulario de registro de usuarios
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()               # Crea el usuario
            return redirect("login")  # Envía al login
    else:
        form = RegisterForm()

    return render(request, "core/register.html", {"form": form})


class DashboardView(LoginRequiredMixin, TemplateView):
    # Muestra el panel principal con estadísticas
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_clientes'] = Client.objects.count()                     # Total clientes
        context['total_vehiculos'] = Vehicle.objects.count()                   # Total vehículos
        context['disponibles'] = Vehicle.objects.filter(estado='available').count()  # Vehículos disponibles
        context['alquilados'] = Rental.objects.filter(estado='activo').count()       # Vehículos alquilados

        context['ingresos_totales'] = Rental.objects.filter(
            estado='finalizado'
        ).aggregate(models.Sum('total'))['total__sum'] or 0                    # Suma de ingresos

        context['mas_alquilados'] = (
            Rental.objects.values('vehiculo__marca', 'vehiculo__modelo')
            .annotate(total=models.Count('id'))
            .order_by('-total')[:5]                                           # Top 5 más alquilados
        )

        return context


class ClientListView(LoginRequiredMixin, ListView):
    # Lista todos los clientes
    model = Client
    template_name = 'core/client_list.html'
    context_object_name = 'clientes'


class ClientCreateView(LoginRequiredMixin, CreateView):
    # Crear cliente
    model = Client
    form_class = ClientForm
    template_name = 'core/client_form.html'


class ClientUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    # Editar cliente (solo admins)
    model = Client
    form_class = ClientForm
    template_name = 'core/client_form.html'


class ClientDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    # Eliminar cliente (solo admins)
    model = Client
    success_url = reverse_lazy('client-list')
    template_name = 'core/delete_confirm.html'


class VehicleListView(LoginRequiredMixin, ListView):
    # Lista todos los vehículos
    model = Vehicle
    template_name = 'core/vehicle_list.html'
    context_object_name = 'vehiculos'


class VehicleCreateView(LoginRequiredMixin, CreateView):
    # Crear vehículo
    model = Vehicle
    form_class = VehicleForm
    template_name = 'core/vehicle_form.html'


class VehicleUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    # Editar vehículo (solo admins)
    model = Vehicle
    form_class = VehicleForm
    template_name = 'core/vehicle_form.html'


class VehicleDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    # Eliminar vehículo (solo admins)
    model = Vehicle
    success_url = reverse_lazy('vehicle-list')
    template_name = 'core/delete_confirm.html'


class RentalListView(LoginRequiredMixin, ListView):
    # Lista los alquileres
    model = Rental
    template_name = 'core/rental_list.html'
    context_object_name = 'rentals'


class RentalCreateView(LoginRequiredMixin, CreateView):
    # Crear alquiler y marcar el vehículo como alquilado
    model = Rental
    form_class = RentalForm
    template_name = 'core/rental_form.html'

    def form_valid(self, form):
        rental = form.save(commit=False)
        vehicle = rental.vehiculo
        vehicle.estado = "rented"      # Marca alquilado
        vehicle.save()
        rental.save()
        return redirect("rental-list")


class RentalUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    # Editar alquiler y actualizar estado del vehículo
    model = Rental
    form_class = RentalForm
    template_name = 'core/rental_form.html'

    def form_valid(self, form):
        rental = form.save(commit=False)
        vehicle = rental.vehiculo

        if rental.estado == "activo":
            vehicle.estado = "rented"
        else:
            vehicle.estado = "available"  # Si el alquiler se finaliza o cancela

        vehicle.save()
        rental.save()
        return redirect("rental-list")


class RentalDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    # Eliminar alquiler y liberar el vehículo
    model = Rental
    success_url = reverse_lazy('rental-list')
    template_name = 'core/delete_confirm.html'

    def delete(self, request, *args, **kwargs):
        rental = self.get_object()
        rental.vehiculo.estado = "available"   # Libera el vehículo
        rental.vehiculo.save()
        return super().delete(request, *args, **kwargs)


class UserLoginView(LoginView):
    # Login del sistema
    template_name = 'core/login.html'
    authentication_form = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy("dashboard")       # Redirige al dashboard


class UserLogoutView(LogoutView):
    # Logout del usuario
    next_page = "login"

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")
