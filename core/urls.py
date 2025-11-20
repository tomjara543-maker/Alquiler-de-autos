from django.urls import path
from .views import (
    DashboardView,
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView,
    VehicleListView, VehicleCreateView, VehicleUpdateView, VehicleDeleteView,
    RentalListView, RentalCreateView, RentalUpdateView, RentalDeleteView,
    UserLoginView, UserLogoutView, register
)

urlpatterns = [
    # Autenticación
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),

    # Dashboard
    path("dashboard/", DashboardView.as_view(), name="dashboard"),

    # Clientes
    path("clients/", ClientListView.as_view(), name="client-list"),
    path("clients/add/", ClientCreateView.as_view(), name="client-add"),
    path("clients/<int:pk>/edit/", ClientUpdateView.as_view(), name="client-edit"),
    path("clients/<int:pk>/delete/", ClientDeleteView.as_view(), name="client-delete"),

    # Vehículos
    path("vehicles/", VehicleListView.as_view(), name="vehicle-list"),
    path("vehicles/add/", VehicleCreateView.as_view(), name="vehicle-add"),
    path("vehicles/<int:pk>/edit/", VehicleUpdateView.as_view(), name="vehicle-edit"),
    path("vehicles/<int:pk>/delete/", VehicleDeleteView.as_view(), name="vehicle-delete"),

    # Alquileres
    path("rentals/", RentalListView.as_view(), name="rental-list"),
    path("rentals/add/", RentalCreateView.as_view(), name="rental-add"),
    path("rentals/<int:pk>/edit/", RentalUpdateView.as_view(), name="rental-edit"),
    path("rentals/<int:pk>/delete/", RentalDeleteView.as_view(), name="rental-delete"),
]
