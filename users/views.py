from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, CustomUserCreationForm
from django.http import HttpResponse

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
            return redirect('dashboard')  # Replace with role-based or generic route

        form.add_error(None, "Invalid username or password")

    if request.headers.get('Hx-Request'):
        return render(request, 'users/templates/users/partials/_login_form.html', {'form': form})

    return render(request, 'users/templates/users/login.html', {'form': form})


def register_view(request):
    form = CustomUserCreationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('users:login')

    if request.headers.get('Hx-Request'):
        return render(request, 'users/templates/users/partials/_register_form.html', {'form': form})

    return render(request, 'users/templates/users/register.html', {'form': form})