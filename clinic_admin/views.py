from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from users.models import CustomUser, MedicoProfile
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from users.forms import LoginForm, CustomUserCreationForm, CustomUserUpdateForm
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from users.models import MedicoProfile, HorarioMedico
from django.template.loader import render_to_string
from users.models import DiaDeAtencion

@login_required
def editar_horarios_medico(request, medico_id):
    DIAS_CHOICES = [
    ('LU', 'Lunes'),
    ('MA', 'Martes'),
    ('MI', 'Miércoles'),
    ('JU', 'Jueves'),
    ('VI', 'Viernes'),
    ('SA', 'Sábado'),
    ('DO', 'Domingo'),
    ]
    medico = get_object_or_404(MedicoProfile, id=medico_id)
    
    # corregido
    if request.user != medico.clinica:
        return HttpResponseBadRequest("No autorizado")

    horarios = HorarioMedico.objects.filter(medico=medico).order_by('dia')

    dias = DiaDeAtencion.DIA_CHOICES

    html = render_to_string("clinic_admin/editar_horarios_medico.html", {
        "medico": medico,
        "horarios": horarios,
        'dias_choices': DIAS_CHOICES,
    }, request=request)

    return JsonResponse({'html': html})


@login_required
def guardar_horarios_medico(request, medico_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido")

    print("POST DATA:", request.POST)

    medico = get_object_or_404(MedicoProfile, id=medico_id)
    if request.user != medico.clinica:
        return HttpResponseForbidden("No autorizado")

    dias = request.POST.getlist('dia[]')
    horas_inicio = request.POST.getlist('hora_inicio[]')
    horas_fin = request.POST.getlist('hora_fin[]')

    print("DIAS:", dias)
    print("HORAS INICIO:", horas_inicio)
    print("HORAS FIN:", horas_fin)

    HorarioMedico.objects.filter(medico=medico).delete()

    for dia, h_inicio, h_fin in zip(dias, horas_inicio, horas_fin):
        HorarioMedico.objects.create(
            medico=medico,
            dia=dia,
            hora_inicio=h_inicio,
            hora_fin=h_fin
        )

    return redirect('clinic_admin:gestionar_medicos')



@login_required
def gestionar_medicos(request):
    if not request.user.is_clinic():
        return HttpResponseBadRequest("No autorizado")

    medicos = MedicoProfile.objects.filter(clinica=request.user)

    return render(request, "clinic_admin/gestionar_medico.html", {
        "medicos": medicos,
        "dias_choices": DiaDeAtencion.DIA_CHOICES
    })

@login_required
def edit_profile_admin(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("clinic_admin:home_admin")
    else:
        form = CustomUserUpdateForm(instance=user)
    return render(request, 'clinic_admin/edit_profile_admin.html', {'form': form})

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