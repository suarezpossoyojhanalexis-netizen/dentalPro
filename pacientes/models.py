from django.db import models
from django.core.validators import RegexValidator

cedula_validator = RegexValidator(
    regex=r'^\d{6,10}$',
    message='La cédula debe tener entre 6 y 10 dígitos.'
)


class Patient(models.Model):
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    DOCUMENT_TYPE_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('TI', 'Tarjeta de Identidad'),
        ('NIT', 'NIT'),
        ('Pasaporte', 'Pasaporte'),
    ]

    first_name = models.CharField('Nombre', max_length=100)
    last_name = models.CharField('Apellido', max_length=100)
    document_type = models.CharField(
        'Tipo de documento', max_length=20, choices=DOCUMENT_TYPE_CHOICES, default='CC'
    )
    cedula = models.CharField('Cédula', max_length=10, unique=True, validators=[cedula_validator])
    occupation = models.CharField('Ocupación', max_length=100, blank=True)
    eps = models.CharField('EPS', max_length=100, blank=True, help_text='EPS o régimen de salud al que pertenece el paciente')
    companion_name = models.CharField('Nombre del acompañante', max_length=100, blank=True)
    companion_phone = models.CharField('Teléfono del acompañante', max_length=15, blank=True)
    birth_date = models.DateField('Fecha de nacimiento')
    phone = models.CharField('Teléfono', max_length=15, blank=True)
    email = models.EmailField('Correo', blank=True)
    address = models.TextField('Dirección', blank=True)
    blood_type = models.CharField('Tipo de sangre', max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True)
    allergies = models.TextField('Alergias', blank=True)
    medical_notes = models.TextField('Notas médicas', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return f'{self.last_name}, {self.first_name} — {self.cedula}'
