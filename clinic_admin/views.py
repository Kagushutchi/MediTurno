from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def home_admin(request):
    if request.user.role not in ['clinic', 'medic']:
        return redirect('users:home')  # Evita que usuarios normales accedan
    return render(request, 'clinic_admin/home_admin.html')
