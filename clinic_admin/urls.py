from django.urls import path
from . import views

app_name = 'clinic_admin'

urlpatterns = [
    path('home/', views.home_admin, name='home_admin'),
    path('home/ficha_pacientes/', views.ficha_pacientes, name='ficha_pacientes'),
    path('home/turnos_pacientes/<int:paciente_id>/', views.turnos_paciente_ajax, name='turnos_paciente_ajax'),
    path('home/cancelar_turno/<int:turno_id>/', views.cancelar_turno, name='cancelar_turno'),
    path('agenda_medicos/', views.medicos_y_turnos_view, name='agenda_medicos'),
]

