from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")


class CustomUserCreationForm(UserCreationForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de Nacimiento"# Usa el selector nativo del navegador
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'nombre', 'apellido', 'dni', 'fecha_nacimiento', 'email', 'password1', 'password2']
        labels = {
            'username': 'Usuario',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'dni': 'DNI',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'email': 'Email',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña'
        }
        # No incluimos 'role'
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Sobreescribir los labels de password1 y password2
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar Contraseña'
    def save(self, commit=True):
        user = super().save(commit=False)
    
    # Asignar automáticamente rol 'user' si no se definió
        if not user.role:
            user.role = 'user'

    # Si es una clínica, limpiar nombre y apellido
        if user.role == 'clinic':
            user.nombre = ''
            user.apellido = ''

        if commit:
            user.save()
        return user

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'nombre', 'apellido', 'email', 'dni', 'fecha_nacimiento', 'telefono',
            'obra_social', 'numero_afiliado', 'ciudad', 'direccion'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

