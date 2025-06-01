from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, ValidationError
from django.utils.timezone import now

def validate_birth_date(value):
    if value > now().date():
        raise ValidationError("La fecha de nacimiento no puede estar en el futuro.")

class CustomUser(AbstractUser):
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
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message="El DNI debe contener exactamente 8 dígitos numéricos",
                code='invalid_dni'
            )
        ]
    )

    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(validators=[validate_birth_date])

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
        max_length=255,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9\s.,#-]+$',
                message="La dirección solo puede contener letras, números, espacios y caracteres especiales básicos.",
                code='invalid_direccion'
            )
        ]
    )

    def is_medic(self):
        return self.role == 'medic'

    def is_clinic(self):
        return self.role == 'clinic'

    def is_admin(self):
        return self.is_superuser