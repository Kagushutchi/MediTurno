from django.shortcuts import render
from django.utils.timezone import now
from appointments.models import Appointment

def notificaciones_turnos(request):
    user = request.user
    print("Usuario autenticado:", user)
    print("Autenticado:", user.is_authenticated)

    if not user.is_authenticated:
        return render(request, 'notifications/lista_notificaciones.html', {
            'turnos': [],
            'mensaje': 'Debes iniciar sesión para ver tus turnos.'
        })

    if user.role != 'user':
        return render(request, 'notifications/lista_notificaciones.html', {
            'turnos': [],
            'mensaje': 'Solo los pacientes pueden ver sus turnos.'
        })

    turnos = Appointment.objects.filter(
        paciente=user,
        fecha_inicio__gte=now(),
        estado__in=['pendiente', 'confirmado']
    ).select_related('medico', 'clinica').order_by('fecha_inicio')

    print("Turnos encontrados:", turnos.count())

    return render(request, 'notifications/lista_notificaciones.html', {'turnos': turnos})

