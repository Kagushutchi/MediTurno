from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, MedicoProfile, Especialidad,DiaDeAtencion
# Import your custom user model

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

@admin.register(MedicoProfile)
class MedicoProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'matricula', 'get_especialidades', 'clinica', 'hora_inicio', 'hora_fin')
    filter_horizontal = ('especialidades', 'dias_que_atiende')
    search_fields = ('user__nombre', 'user__apellido', 'matricula')
    list_filter = ('clinica',)
    
    def get_dias_de_atencion(self, obj):
        return ", ".join([str(dia) for dia in obj.dias_de_atencion.all()])
    get_dias_de_atencion.short_description = "Días de Atención"

    def get_especialidades(self, obj):
        return ", ".join([e.nombre for e in obj.especialidades.all()])
    get_especialidades.short_description = 'Especialidades'


admin.site.register(CustomUser, CustomUserAdmin)