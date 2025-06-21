from django.db import models
from django.conf import settings
from users.models import CustomUser

class Appointment(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('completado', 'Completado'),
    ]

    paciente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='turnos_paciente',
        limit_choices_to={'role': 'user'}
    )
    medico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='turnos_medico',
        limit_choices_to={'role': 'medic'}
    )
    clinica = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='turnos_clinica',
        limit_choices_to={'role': 'clinic'}
    )
    
    

    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    motivo = models.TextField(blank=True, null=True)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"

    def __str__(self):
        return f"{self.paciente} con {self.medico} en {self.clinica} - {self.fecha_inicio}"
 
