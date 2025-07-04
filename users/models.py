from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, ValidationError
from django.utils.timezone import now
from django.contrib.auth.models import BaseUserManager

#dias
class DiaDeAtencion(models.Model):
    DIA_CHOICES = [
        ('LU', 'Lunes'),
        ('MA', 'Martes'),
        ('MI', 'Miércoles'),
        ('JU', 'Jueves'),
        ('VI', 'Viernes'),
        ('SA', 'Sábado'),
        ('DO', 'Domingo'),
    ]
    codigo = models.CharField(max_length=2, choices=DIA_CHOICES, unique=True)

    def __str__(self):
        return dict(self.DIA_CHOICES)[self.codigo]


def validate_birth_date(value):
    if value > now().date():
        raise ValidationError("La fecha de nacimiento no puede estar en el futuro.")

#Esta clase es para poder crear el super admin si necesidad de agregar todos los campos
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

#Aca esta el usuario base
class CustomUser(AbstractUser):
    objects = CustomUserManager()
    
    USER_TYPES = (
        ('user', 'User'),
        ('medic', 'Medic'),
        ('clinic', 'Clinic'),
    )
    OBRA_SOCIAL_CHOICES = (
        ('osde', 'OSDE'),
        ('swiss_medical', 'Swiss Medical'),
        ('galeno', 'Galeno'),
        ('medife', 'Medifé'),
        ('other', 'Other')
    )
    CIUDAD_CHOICES = (
        ('villa_gesell', 'Villa Gesell'),
        ('pinamar', 'Pinamar'),
        ('madariaga', 'Madariaga'),
    )

    role = models.CharField(max_length=10, choices=USER_TYPES, default='user', blank=True, null=True)

    obra_social = models.CharField(
        max_length=20,
        choices=OBRA_SOCIAL_CHOICES,
        default='other',
        blank=True,
        null=True
    )

    numero_afiliado = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{8,12}$',
                message="Número de afiliado debe contener entre 8 y 12 dígitos numéricos",
                code='invalid_numero_afiliado'
            )
        ]
    )

    dni = models.CharField(
        max_length=8,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message="El DNI debe contener exactamente 8 dígitos numéricos",
                code='invalid_dni'
            )
        ]
    )

    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50,blank=True,null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField(validators=[validate_birth_date], blank=True, null=True)

    telefono = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{7,15}$',
                message="El teléfono debe contener entre 7 y 15 dígitos, opcionalmente con un prefijo internacional.",
                code='invalid_telefono'
            )
        ]
    )

    ciudad = models.CharField(
        max_length=50,
        choices=CIUDAD_CHOICES,
        default='villa_gesell',
        blank=True,
        null=True
    )

    direccion = models.CharField(
        max_length=2048,
        blank=True,
        null=True
    )

    def is_medic(self):
        return self.role == 'medic'

    def is_clinic(self):
        return self.role == 'clinic'

    def is_admin(self):
        return self.is_superuser
    
class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class MedicoProfile(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='medico_profile')
    especialidades = models.ManyToManyField('Especialidad', related_name='medicos')
    clinica = models.ForeignKey(
        'CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'clinic'},
        related_name='medicos_en_clinica'
    )
    matricula = models.CharField(max_length=30)

    def __str__(self):
        return f"Dr. {self.user.nombre} {self.user.apellido} - {', '.join([e.nombre for e in self.especialidades.all()])}"
"""
    def clean(self):
        # Si ya existe, validamos que tenga al menos un horario
        if self.pk and not self.horarios.exists():
            raise ValidationError("El medico debe tener al menos un horario cargado.")
"""
class ClinicaProfile(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='clinica_profile')
    nombre_comercial = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.nombre_comercial
"""
    def clean(self):
        # Si ya existe, validamos que tenga al menos un horario
        if self.pk and not self.horarios.exists():
            raise ValidationError("La clínica debe tener al menos un horario cargado.")
"""
#Es para hacer los horarios de las clinicas y que puedan ser asimetricos ej: de LU a VI un horario y los SA otro:

class HorarioClinica(models.Model):
    clinica = models.ForeignKey('ClinicaProfile', on_delete=models.CASCADE, related_name='horarios')
    dia = models.CharField(max_length=2, choices=DiaDeAtencion.DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        unique_together = ('clinica', 'dia')

    def __str__(self):
        return f"{self.get_dia_display()}: {self.hora_inicio} - {self.hora_fin}"

class HorarioMedico(models.Model):
    medico = models.ForeignKey('MedicoProfile', on_delete=models.CASCADE, related_name='horarios')
    dia = models.CharField(max_length=2, choices=DiaDeAtencion.DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        unique_together = ('medico', 'dia')

    def __str__(self):
        return f"{self.get_dia_display()}: {self.hora_inicio} - {self.hora_fin}"

