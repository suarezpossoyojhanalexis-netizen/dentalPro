from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q
from .models import Patient
from .forms import PatientForm


class PatientListView(ListView):
    model = Patient
    template_name = 'pacientes/lista.html'
    context_object_name = 'patients'
    paginate_by = 20

    def get_queryset(self):
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


class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'pacientes/formulario.html'
    success_url = reverse_lazy('pacientes:lista')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['accion'] = 'Nuevo'
        return ctx


class PatientDetailView(DetailView):
    model = Patient
    template_name = 'pacientes/detalle.html'
    context_object_name = 'patient'

    def get_queryset(self):
        return Patient.objects.filter(is_active=True)


class PatientUpdateView(UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'pacientes/formulario.html'
    success_url = reverse_lazy('pacientes:lista')

    def get_queryset(self):
        return Patient.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['accion'] = 'Editar'
        return ctx


class PatientDeleteView(DeleteView):
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
        return HttpResponseRedirect(self.get_success_url())
