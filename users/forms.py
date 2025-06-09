from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CustomUserCreationForm(UserCreationForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Usa el selector nativo del navegador
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'nombre', 'apellido', 'dni', 'fecha_nacimiento', 'email', 'password1', 'password2']  # No incluimos 'role'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'user'  # Asignamos automáticamente el rol "User"
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
