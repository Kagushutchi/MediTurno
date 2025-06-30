from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, CustomUserCreationForm, CustomUserUpdateForm
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm 
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import CustomUser

def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)
            return redirect('users:home')  # Replace with role-based or generic route

        form.add_error(None, "Invalid username or password")

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

@login_required(login_url='/users/login/')
def map_view(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    return render(request, 'users/map.html', {'direccion': user.direccion})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users:home")
    else:
        form = CustomUserUpdateForm(instance=user)
    return render(request, 'users/edit_profile.html', {'form': form})
