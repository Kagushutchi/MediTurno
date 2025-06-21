from django.urls import path
from .views import login_view, register_view, home_view
from appointments.views import buscar_medicos

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('home/', home_view, name='home'),
    path('home/appointments', buscar_medicos, name='buscar_medico'),
]