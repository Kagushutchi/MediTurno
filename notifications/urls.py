from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notificaciones_turnos, name='lista_notificaciones'),
]
