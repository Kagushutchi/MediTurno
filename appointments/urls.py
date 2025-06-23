from django.urls import path
from . import views
from .views import buscar_medicos

app_name = 'appointments'

urlpatterns = [
    path('buscar/', views.buscar_medicos, name='buscar_medicos'),
    # Puedes agregar otras rutas relacionadas a turnos o citas aquí
    path('medico/<int:medico_id>/horarios/', views.obtener_horarios_medico, name='obtener_horarios_medico'),
    path('crear_turno/', views.crear_turno, name='crear_turno'),
    path('confirmacion/', views.confirmacion_turno, name='confirmacion_turno'),
    ]
