python manage.py shell

from users.models import DiaDeAtencion

dias = [
    ('LU', 'Lunes'),
    ('MA', 'Martes'),
    ('MI', 'Miércoles'),
    ('JU', 'Jueves'),
    ('VI', 'Viernes'),
    ('SA', 'Sábado'),
    ('DO', 'Domingo'),
]

for codigo, nombre in dias:
    DiaDeAtencion.objects.get_or_create(codigo=codigo)
