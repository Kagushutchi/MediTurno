
# Register your models here.
from django.contrib import admin
from .models import Appointment
from users.models import Especialidad

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'paciente',
        'medico',
        'clinica',
        'fecha_inicio',
        'fecha_fin',
        'estado',
        'creado',
    )
    list_filter = (
        'estado',
        'fecha_inicio',
        'clinica',
    )
    search_fields = (
        'paciente__nombre',
        'paciente__apellido',
        'medico__nombre',
        'medico__apellido',
        'clinica__clinica_profile__nombre_comercial',
        'motivo',
    )
    date_hierarchy = 'fecha_inicio'
    ordering = ['-fecha_inicio']
    autocomplete_fields = ['paciente', 'medico', 'clinica']
