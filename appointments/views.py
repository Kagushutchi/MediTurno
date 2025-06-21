from django.shortcuts import render
from django.db.models import Q
from users.models import CustomUser, Especialidad, MedicoProfile



def buscar_medicos(request):
    query = request.GET.get('q', '')
    
    clinica_name = request.GET.get('clinica', '')
    especialidad = request.GET.get('especialidad', '')
    localidad = request.GET.get('localidad', '')

    # Iniciamos la query con todos los perfiles de médicos
    medicos = MedicoProfile.objects.all()

    if query:
        medicos = medicos.filter(
            Q(user__nombre__icontains=query) | Q(user__apellido__icontains=query)
        )
    if clinica_name:
        # Se filtra a partir del nombre comercial que se encuentra en el ClinicaProfile vinculado
        medicos = medicos.filter(clinica__clinica_profile__nombre_comercial=clinica_name)
    if especialidad:
        medicos = medicos.filter(especialidad__nombre=especialidad)
    if localidad:
        medicos = medicos.filter(user__ciudad=localidad)

    # Se obtienen los filtros dinámicos para clínicas y especialidades
    clinicas = CustomUser.objects.filter(role='clinic')
    especialidades = Especialidad.objects.all()

    context = {
        'medicos': medicos,
        'clinicas': clinicas,
        'especialidades': especialidades,
    }
    return render(request, 'appointments/buscar_medicos.html', context)

