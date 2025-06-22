from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from users.models import MedicoProfile, Especialidad, CustomUser, HorarioMedico
from .models import Appointment
from datetime import datetime, timedelta
from collections import defaultdict
from django.http import JsonResponse
from django.template.loader import render_to_string

def buscar_medicos(request):
    query = request.GET.get('q', '')
    clinica_name = request.GET.get('clinica', '')
    especialidad = request.GET.get('especialidad', '')
    localidad = request.GET.get('localidad', '')

    medicos = MedicoProfile.objects.select_related('user', 'clinica').prefetch_related('especialidades')

    if query:
        medicos = medicos.filter(
            Q(user__nombre__icontains=query) |
            Q(user__apellido__icontains=query)
        )

    if clinica_name:
        medicos = medicos.filter(
            clinica__clinica_profile__nombre_comercial__icontains=clinica_name
        )

    if especialidad:
        medicos = medicos.filter(especialidades__nombre__icontains=especialidad)

    if localidad:
        medicos = medicos.filter(user__ciudad=localidad)

    clinicas = CustomUser.objects.filter(role='clinic')
    especialidades = Especialidad.objects.all()

    context = {
        'medicos': medicos,
        'clinicas': clinicas,
        'especialidades': especialidades,
    }
    return render(request, 'appointments/buscar_medicos.html', context)

def obtener_horarios_medico(request, medico_id):
    medico = get_object_or_404(MedicoProfile, id=medico_id)
    horarios = HorarioMedico.objects.filter(medico=medico)
    turnos_tomados = Appointment.objects.filter(
        medico=medico.user,
        estado__in=['pendiente', 'confirmado']
    )

    horas_ocupadas = set(t.fecha_inicio for t in turnos_tomados)

    from datetime import datetime, timedelta
    from collections import defaultdict

    DIAS_MAPA = {
        'MO': 'LU',
        'TU': 'MA',
        'WE': 'MI',
        'TH': 'JU',
        'FR': 'VI',
        'SA': 'SA',
        'SU': 'DO',
    }

    disponibilidad = defaultdict(list)
    hoy = datetime.now()

    for i in range(7):
        dia = hoy + timedelta(days=i)
        dia_abrev = dia.strftime('%a').upper()[:2]
        dia_codigo = DIAS_MAPA.get(dia_abrev)
        if not dia_codigo:
            continue  # Por si hay un día que no mapea

        for horario in horarios:
            if horario.dia == dia_codigo:
                hora_actual = datetime.combine(dia.date(), horario.hora_inicio)
                fin = datetime.combine(dia.date(), horario.hora_fin)
                while hora_actual < fin:
                    if hora_actual not in horas_ocupadas:
                        disponibilidad[dia.date()].append(hora_actual.time())
                    hora_actual += timedelta(minutes=30)

    html = render_to_string('appointments/horarios_medico.html', {
        'medico': medico,
        'disponibilidad': dict(disponibilidad)
    })
    return JsonResponse({'html': html})
