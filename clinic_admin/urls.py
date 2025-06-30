from django.urls import path
from . import views

app_name = 'clinic_admin'

urlpatterns = [
    path('home/', views.home_admin, name='home_admin'),
]
