from django.urls import path
from .views import login_view, register_view, home_view, map_view, edit_profile, logout_view, suggest_turno_view
from appointments.views import buscar_medicos

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('home/', home_view, name='home'),
    path('map/<int:user_id>/', map_view, name='map'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('logout/', logout_view, name='logout'),
    path('home/appointments', buscar_medicos, name='buscar_medico'),
    path('suggest_turno/', suggest_turno_view, name='suggest_turno'),
]