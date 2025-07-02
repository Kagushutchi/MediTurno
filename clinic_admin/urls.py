from django.urls import path
from . import views

app_name = 'clinic_admin'

urlpatterns = [
    path('home/', views.home_admin, name='home_admin'),
    path('edit_profile_admin/', views.edit_profile_admin, name='edit_profile_admin'),
    path('home/ficha_pacientes/', views.ficha_pacientes, name='ficha_pacientes'),
    path('home/turnos_pacientes/<int:paciente_id>/', views.turnos_paciente_ajax, name='turnos_paciente_ajax'),
    path('home/cancelar_turno/<int:turno_id>/', views.cancelar_turno, name='cancelar_turno'),
    path('agenda_medicos/', views.medicos_y_turnos_view, name='agenda_medicos'),
    path("medico/<int:medico_id>/editar_horarios/", views.editar_horarios_medico, name="editar_horarios_medico"),
    path("medico/<int:medico_id>/guardar_horarios/", views.guardar_horarios_medico, name="guardar_horarios_medico"),
    path("gestionar_medicos/", views.gestionar_medicos, name="gestionar_medicos"),
]

