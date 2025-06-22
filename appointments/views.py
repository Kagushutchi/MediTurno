from django.shortcuts import render
from django.db.models import Q
from users.models import MedicoProfile, Especialidad, CustomUser

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
