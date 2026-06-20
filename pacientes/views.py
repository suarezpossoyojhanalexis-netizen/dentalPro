from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from .models import Patient
from .forms import PatientForm


class PatientListView(ListView):
    # Muestra la lista de pacientes activos con paginación y búsqueda
    model = Patient
    template_name = 'pacientes/lista.html'
    context_object_name = 'patients'
    paginate_by = 20

    def get_queryset(self):
        # Si el usuario escribió algo en el buscador, filtra por nombre, cédula o teléfono
        q = self.request.GET.get('q', '').strip()
        qs = Patient.objects.filter(is_active=True)
        if q:
            qs = qs.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(cedula__icontains=q) |
                Q(phone__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class PatientCreateView(SuccessMessageMixin, CreateView):
    # Formulario para registrar un paciente nuevo
    model = Patient
    form_class = PatientForm
    template_name = 'pacientes/formulario.html'
    success_url = reverse_lazy('pacientes:lista')
    success_message = 'Paciente creado exitosamente.'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['accion'] = 'Nuevo'
        return ctx


class PatientDetailView(DetailView):
    # Muestra la ficha completa de un paciente (solo si está activo)
    model = Patient
    template_name = 'pacientes/detalle.html'
    context_object_name = 'patient'

    def get_queryset(self):
        return Patient.objects.filter(is_active=True)


class PatientUpdateView(SuccessMessageMixin, UpdateView):
    # Formulario para editar los datos de un paciente existente
    model = Patient
    form_class = PatientForm
    template_name = 'pacientes/formulario.html'
    success_url = reverse_lazy('pacientes:lista')
    success_message = 'Paciente actualizado exitosamente.'

    def get_queryset(self):
        return Patient.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['accion'] = 'Editar'
        return ctx


class PatientDeleteView(DeleteView):
    # Soft delete: marca al paciente como inactivo en vez de borrarlo
    model = Patient
    template_name = 'pacientes/confirmar_eliminar.html'
    context_object_name = 'patient'
    success_url = reverse_lazy('pacientes:lista')

    def get_queryset(self):
        return Patient.objects.filter(is_active=True)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save(update_fields=['is_active'])
        messages.success(request, 'Paciente eliminado (desactivado) exitosamente.')
        return HttpResponseRedirect(self.get_success_url())
