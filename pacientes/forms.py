from django import forms
from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'document_type', 'cedula', 'birth_date',
            'phone', 'email', 'address', 'blood_type',
            'allergies', 'medical_notes',
        ]
        widgets = {
            'birth_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent'}
            ),
            'address': forms.Textarea(
                attrs={'rows': 3, 'class': 'w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent'}
            ),
            'allergies': forms.Textarea(
                attrs={'rows': 3, 'class': 'w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent'}
            ),
            'medical_notes': forms.Textarea(
                attrs={'rows': 3, 'class': 'w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        text_input_fields = ['first_name', 'last_name', 'cedula', 'phone', 'email']
        for field_name in text_input_fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent'
            })
        choice_fields = ['document_type', 'blood_type']
        for field_name in choice_fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent'
            })
