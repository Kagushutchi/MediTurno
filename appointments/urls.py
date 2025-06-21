from django.urls import path
from . import views
from .views import buscar_medicos

app_name = 'appointments'

urlpatterns = [
    path('buscar/', views.buscar_medicos, name='buscar_medicos'),
    # Puedes agregar otras rutas relacionadas a turnos o citas aquí
]
