from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    # Configuración del panel de administración de Django para pacientes
    list_display = ['last_name', 'first_name', 'document_type', 'cedula', 'occupation', 'eps', 'phone', 'companion_name', 'is_active']
    list_filter = ['is_active', 'blood_type', 'document_type']
    search_fields = ['first_name', 'last_name', 'cedula', 'phone']
