from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db import models
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .forms import CustomLoginForm, RegisterForm, ClientForm, VehicleForm, RentalForm
from .models import Client, Vehicle, Rental


# ===========================
# PERMISOS (solo superusuario)
# ===========================
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('dashboard')


# ================
# REGISTRO
# ================
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "core/register.html", {"form": form})


# ================
# DASHBOARD
# ================
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_clientes'] = Client.objects.count()
        context['total_vehiculos'] = Vehicle.objects.count()
        context['disponibles'] = Vehicle.objects.filter(estado='available').count()
        context['alquilados'] = Rental.objects.filter(estado='activo').count()

        context['ingresos_totales'] = Rental.objects.filter(
            estado='finalizado'
        ).aggregate(models.Sum('total'))['total__sum'] or 0

        context['mas_alquilados'] = (
            Rental.objects.values('vehiculo__marca', 'vehiculo__modelo')
            .annotate(total=models.Count('id'))
            .order_by('-total')[:5]
        )

        return context


# ==================
# CLIENTES CRUD
# ==================
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'core/client_list.html'
    context_object_name = 'clientes'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'core/client_form.html'


class ClientUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'core/client_form.html'


class ClientDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client-list')
    template_name = 'core/delete_confirm.html'


# ==================
# VEHÍCULOS CRUD
# ==================
class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = 'core/vehicle_list.html'
    context_object_name = 'vehiculos'


class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'core/vehicle_form.html'


class VehicleUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'core/vehicle_form.html'


class VehicleDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Vehicle
    success_url = reverse_lazy('vehicle-list')
    template_name = 'core/delete_confirm.html'


# ==================
# ALQUILERES CRUD
# ==================
class RentalListView(LoginRequiredMixin, ListView):
    model = Rental
    template_name = 'core/rental_list.html'
    context_object_name = 'rentals'


class RentalCreateView(LoginRequiredMixin, CreateView):
    model = Rental
    form_class = RentalForm
    template_name = 'core/rental_form.html'

    def form_valid(self, form):
        rental = form.save(commit=False)
        vehicle = rental.vehiculo

        vehicle.estado = "rented"
        vehicle.save()

        rental.save()
        return redirect("rental-list")


class RentalUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Rental
    form_class = RentalForm
    template_name = 'core/rental_form.html'

    def form_valid(self, form):
        rental = form.save(commit=False)
        vehicle = rental.vehiculo

        if rental.estado == "activo":
            vehicle.estado = "rented"
        else:
            vehicle.estado = "available"

        vehicle.save()
        rental.save()

        return redirect("rental-list")


class RentalDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Rental
    success_url = reverse_lazy('rental-list')
    template_name = 'core/delete_confirm.html'

    def delete(self, request, *args, **kwargs):
        rental = self.get_object()
        rental.vehiculo.estado = "available"
        rental.vehiculo.save()
        return super().delete(request, *args, **kwargs)


# ==================
# LOGIN / LOGOUT
# ==================
class UserLoginView(LoginView):
    template_name = 'core/login.html'
    authentication_form = CustomLoginForm

    def get_success_url(self):
        return reverse_lazy("dashboard")


class UserLogoutView(LogoutView):
    next_page = "login"

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")
