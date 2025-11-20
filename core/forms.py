from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Client, Vehicle, Rental


# ==========================================================
#  FORMULARIO DE REGISTRO (UserCreationForm con Bootstrap)
# ==========================================================
class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": field.label,
                "autocomplete": "off"
            })


# ==========================================================
#  LOGIN FORM PERSONALIZADO (AuthenticationForm con Bootstrap)
# ==========================================================
class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": field.label,
                "autocomplete": "off"
            })


# ==========================================================
#  CLIENTE
# ==========================================================
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


# ==========================================================
#  VEHÍCULO
# ==========================================================
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


# ==========================================================
#  ALQUILER – VERSIÓN ORIGINAL QUE TE FUNCIONABA BIEN
# ==========================================================
class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = "__all__"
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-select"}),
            "vehiculo": forms.Select(attrs={"class": "form-select"}),
            "fecha_inicio": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "monto": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # VERSIÓN ORIGINAL → No se filtra nada
        self.fields["vehiculo"].queryset = Vehicle.objects.all()

        # Bootstrap en los demás campos
        for field_name, field in self.fields.items():
            if not field.widget.attrs.get("class"):
                if isinstance(field.widget, forms.Select):
                    field.widget.attrs["class"] = "form-select"
                else:
                    field.widget.attrs["class"] = "form-control"
