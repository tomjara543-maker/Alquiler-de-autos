from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Cuando el usuario visita "/": redirige a login
    path('', redirect_to_login),

    # Todas las rutas del sistema (login, dashboard, etc.)
    path('', include('core.urls')),
]
