from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ValidationError
from .models import CustomUser, MedicoProfile, ClinicaProfile, Especialidad, DiaDeAtencion, HorarioClinica, HorarioMedico

class HorarioClinicaInline(admin.TabularInline):
    model = HorarioClinica
    extra = 1  # Cantidad de líneas vacías por defecto
    verbose_name = "Horario por Día"
    verbose_name_plural = "Horarios de Atención"

@admin.register(ClinicaProfile)
class ClinicaProfileAdmin(admin.ModelAdmin):
    list_display = ('nombre_comercial', 'razon_social', 'get_dias_de_atencion')
    search_fields = ('nombre_comercial', 'razon_social')
    inlines = [HorarioClinicaInline]

    def get_dias_de_atencion(self, obj):
        dias = obj.horarios.all()
        return ", ".join(dict(DiaDeAtencion.DIA_CHOICES).get(d.dia, d.dia) for d in dias)

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'nombre', 'apellido', 'dni', 'is_staff', 'is_superuser', 'role')  # Display relevant fields
    search_fields = ('email', 'username', 'nombre', 'apellido', 'dni')  # Enable search by key attributes
    ordering = ('email',)  # Order users by email

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Information', {'fields': ('nombre', 'apellido', 'fecha_nacimiento', 'telefono', 'dni', 'ciudad', 'direccion')}),
        ('Medical Info', {'fields': ('obra_social', 'numero_afiliado')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'role')}),
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'username', 'password1', 'password2')}),
        ('Personal Information', {'fields': ('nombre', 'apellido', 'fecha_nacimiento', 'telefono', 'dni', 'ciudad', 'direccion')}),
        ('Medical Info', {'fields': ('obra_social', 'numero_afiliado')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'role')}),
    )

    @admin.display(description="User Role")
    def get_role(self, obj):
        return obj.role.capitalize()

class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)      # Muestra el campo 'nombre' en el listado
    search_fields = ('nombre',)     # Agrega una barra de búsqueda por 'nombre'

admin.site.register(Especialidad, EspecialidadAdmin)

class HorarioMedicoInline(admin.TabularInline):
    model = HorarioMedico
    extra = 1  # Cantidad de líneas vacías por defecto
    verbose_name = "Horario por Día"
    verbose_name_plural = "Horarios de Atención"

@admin.register(MedicoProfile)
class MedicoProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'matricula', 'get_especialidades', 'clinica', 'get_dias_de_atencion')
    filter_horizontal = ('especialidades',)
    search_fields = ('user__nombre', 'user__apellido', 'matricula')
    list_filter = ('clinica',)
    inlines = [HorarioMedicoInline]
    
    def get_dias_de_atencion(self, obj):
        dias = obj.horarios.all()
        return ", ".join(dict(DiaDeAtencion.DIA_CHOICES).get(d.dia, d.dia) for d in dias)

    def get_especialidades(self, obj):
        return ", ".join([e.nombre for e in obj.especialidades.all()])
    get_especialidades.short_description = 'Especialidades'

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(DiaDeAtencion)
