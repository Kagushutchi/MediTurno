from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from users.models import CustomUser, MedicoProfile
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt



@login_required
def home_admin(request):
    if request.user.role not in ['clinic', 'medic']:
        return redirect('users:home')  # Evita que usuarios normales accedan
    return render(request, 'clinic_admin/home_admin.html')

@login_required
def ficha_pacientes(request):
    if request.user.role != 'clinic':
        return redirect('users:home')

    # Buscar pacientes con turnos en la clínica
    query = request.GET.get('q', '')
    turnos = Appointment.objects.filter(clinica=request.user).select_related('paciente')

    if query:
        turnos = turnos.filter(
            Q(paciente__nombre__icontains=query) |
            Q(paciente__apellido__icontains=query)
        )

    # Solo pacientes únicos
    pacientes = {t.paciente for t in turnos}

    context = {
        'pacientes': pacientes,
    }
    return render(request, 'clinic_admin/ficha_pacientes.html', context)

@login_required
def turnos_paciente_ajax(request, paciente_id):
    if request.user.role != 'clinic':
        return HttpResponse(status=403)

    paciente = get_object_or_404(CustomUser, id=paciente_id)
    turnos = Appointment.objects.filter(
        paciente=paciente,
        clinica=request.user
    ).order_by('-fecha_inicio')

    html = render_to_string('clinic_admin/partials/turnos_pacientes.html', {
        'turnos': turnos,
        'paciente': paciente
    }, request=request)

    return HttpResponse(html)

@csrf_exempt
@login_required
def cancelar_turno(request, turno_id):
    if request.method == "POST":
        turno = get_object_or_404(Appointment, id=turno_id, clinica=request.user)
        turno.estado = 'cancelado'
        turno.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def medicos_y_turnos_view(request):
    clinic_user = request.user
    
    medicos = MedicoProfile.objects.filter(clinica=clinic_user)

    medicos_con_turnos = []
    for medico in medicos:
        turnos = Appointment.objects.filter(medico=medico.user)
        medicos_con_turnos.append({
            'medico': medico,
            'turnos': turnos,
        })
    return render(request, 'clinic_admin/agenda_medicos.html', {
        'medicos_con_turnos': medicos_con_turnos,
    })

