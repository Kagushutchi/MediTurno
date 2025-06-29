from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, CustomUserCreationForm
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm 
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is not None:
            login(request, user)  # 👈 Esto es lo que faltaba
            if user.role in ['clinic', 'medic']:
                return redirect('clinic_admin:home_admin')
            else:
                return redirect('users:home')
        else:
            form.add_error(None, "Nombre de usuario o contraseña incorrectos")


    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Se guarda con rol 'user'
            login(request, user)  # Iniciar sesión después del registro
            return redirect("users:login")  # Redirigir a la página principal
    else:
        form = CustomUserCreationForm()

    return render(request, "users/register.html", {"form": form})


# en users/views.py


def logout_view(request):
    logout(request)
    return redirect('users:login')

@login_required(login_url='/users/login/')
def home_view(request):
    return render(request, 'users/home.html')
