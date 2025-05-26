from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('user', 'User'),
        ('medic', 'Medic'),
        ('clinic', 'Clinic'),
    )
    role = models.CharField(max_length=10, choices=USER_TYPES, default='user')

    def is_medic(self):
        return self.role == 'medic'

    def is_clinic(self):
        return self.role == 'clinic'

    def is_admin(self):
        return self.is_superuser