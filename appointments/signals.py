# en users/signals.py o similar
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from users.models import DiaDeAtencion

@receiver(post_migrate)
def crear_dias(sender, **kwargs):
    dias = [
        ('LU', 'Lunes'),
        ('MA', 'Martes'),
        ('MI', 'Miércoles'),
        ('JU', 'Jueves'),
        ('VI', 'Viernes'),
        ('SA', 'Sábado'),
        ('DO', 'Domingo'),
    ]
    for codigo, _ in dias:
        DiaDeAtencion.objects.get_or_create(codigo=codigo)
