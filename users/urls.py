from django.urls import path
from .views import login_view, register_view, home_view, map_view

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('home/', home_view, name='home'),
    path('map/', map_view, name='map')
]