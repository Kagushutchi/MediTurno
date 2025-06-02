from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, CustomUserCreationForm
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm 
from django.urls import reverse
from django.contrib.auth.decorators import login_required


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

@login_required(login_url='/users/login/')
def home_view(request):
    return render(request, 'users/home.html')

@login_required(login_url='/users/login/')
def map_view(request):
    return render(request, 'users/map.html')