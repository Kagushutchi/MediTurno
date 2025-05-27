from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']  # No incluimos 'role'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'user'  # Asignamos automáticamente el rol "User"
        if commit:
            user.save()
        return user