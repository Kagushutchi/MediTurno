from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, CustomUserCreationForm, CustomUserUpdateForm
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm 
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import CustomUser
from appointments.models import Appointment
from datetime import timedelta

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

@login_required(login_url='/users/login/')
def map_view(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    return render(request, 'users/map.html', {'direccion': user.direccion})

@login_required(login_url='/users/login/')
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

@login_required(login_url='/users/login/')
def suggest_turno_view(request):
    user = request.user
    medic_ids = Appointment.objects.filter(paciente=user).values_list('medico_id', flat=True)
    unique_medic_ids = set(medic_ids)  # This ensures each medic is only processed once
    suggestions = []

    for medic_id in unique_medic_ids:
        medic = CustomUser.objects.get(id=medic_id)
        turns = Appointment.objects.filter(paciente=user, medico_id=medic_id).order_by('-fecha_inicio')[:3]
        turns = list(turns)
        suggested_date = None

        if len(turns) >= 2:
            intervals = [
                (turns[i].fecha_inicio - turns[i+1].fecha_inicio).days
                for i in range(len(turns)-1)
            ]
            avg_interval = sum(intervals) // len(intervals)
            suggested_date = turns[0].fecha_inicio + timedelta(days=avg_interval)

        suggestions.append({
            'medic': medic,
            'turns': turns,
            'suggested_date': suggested_date,
        })

    return render(request, 'users/suggest_turno.html', {
        'suggestions': suggestions,
    })

