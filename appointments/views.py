from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from users.models import MedicoProfile, Especialidad, CustomUser, HorarioMedico
from .models import Appointment
from datetime import datetime, timedelta
from collections import defaultdict
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.timezone import localtime
from django.http import HttpResponseBadRequest



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

    # Horarios ocupados como datetime
    horas_ocupadas = set(localtime(t.fecha_inicio).replace(second=0, microsecond=0) for t in turnos_tomados)

    # Mapeo de código de día del sistema (MO, TU...) al formato del modelo (LU, MA...)
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

    for i in range(60):  # Recorremos 60 días (2 meses)
        dia = hoy + timedelta(days=i)
        dia_abrev = dia.strftime('%a').upper()[:2]
        dia_codigo = DIAS_MAPA.get(dia_abrev)
        if not dia_codigo:
            continue

        horarios_en_dia = horarios.filter(dia=dia_codigo)
        if not horarios_en_dia.exists():
            continue  # Si ese día no atiende, lo salteamos

        horarios_disponibles = []
        for horario in horarios_en_dia:
            hora_actual = datetime.combine(dia.date(), horario.hora_inicio)
            fin = datetime.combine(dia.date(), horario.hora_fin)

            while hora_actual < fin:
                if hora_actual not in horas_ocupadas:
                    horarios_disponibles.append(hora_actual.time())
                hora_actual += timedelta(minutes=30)

        # ⛔ Si no tiene horarios disponibles ese día, NO lo agregamos
        if horarios_disponibles:
            disponibilidad[dia.date()] = horarios_disponibles

    html = render_to_string('appointments/horarios_medico.html', {
        'medico': medico,
        'disponibilidad': dict(disponibilidad),
    }, request=request)

    return JsonResponse({'html': html})





@login_required
def crear_turno(request):
    if request.method == 'POST':
        medico_id = request.POST.get('medico_id')
        fecha = request.POST.get('fecha')  
        hora = request.POST.get('hora')    

        medico = get_object_or_404(MedicoProfile, id=medico_id)
        paciente = request.user

        try:
            fecha_inicio = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return HttpResponseBadRequest("Formato de fecha u hora incorrecto.")

        fecha_fin = fecha_inicio + timedelta(minutes=30)

        # 🚫 Verificar si ya está tomado
        ya_tomado = Appointment.objects.filter(
            medico=medico.user,
            fecha_inicio=fecha_inicio,
            estado__in=['pendiente', 'confirmado']
        ).exists()

        if ya_tomado:
            return HttpResponseBadRequest("Ese horario ya fue tomado. Por favor, seleccioná otro.")

        Appointment.objects.create(
            paciente=paciente,
            medico=medico.user,
            clinica=medico.clinica,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado='pendiente'
        )

        return redirect('appointments:confirmacion_turno')

    return redirect('appointments:buscar_medicos')



@login_required
def confirmacion_turno(request):
    return render(request, 'appointments/confirmacion_turno.html')
