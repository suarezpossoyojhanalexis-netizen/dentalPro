import datetime
from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from pacientes.models import Patient


class PatientModelTest(TestCase):
    # Pruebas sobre el modelo Patient: creación, validaciones, valores por defecto
    def setUp(self):
        # Datos base para crear pacientes en las pruebas
        self.data = {
            'first_name': 'Ana',
            'last_name': 'García',
            'document_type': 'CC',
            'cedula': '123456789',
            'birth_date': datetime.date(1985, 7, 22),
            'phone': '3001112233',
            'email': 'ana@example.com',
            'blood_type': 'O+',
        }

    def test_create_valid_patient(self):
        # Crea un paciente con datos válidos y verifica que existe
        p = Patient.objects.create(**self.data)
        self.assertEqual(Patient.objects.count(), 1)
        self.assertTrue(p.is_active)

    def test_cedula_less_than_5_digits_fails(self):
        # Un número de documento con menos de 5 dígitos debe dar error
        p = Patient(**{**self.data, 'cedula': '1234'})
        with self.assertRaises(ValidationError):
            p.full_clean()

    def test_cedula_more_than_15_digits_fails(self):
        # Un número de documento con más de 15 dígitos debe dar error
        p = Patient(**{**self.data, 'cedula': '1234567890123456'})
        with self.assertRaises(ValidationError):
            p.full_clean()

    def test_cedula_duplicate_fails(self):
        # No se pueden crear dos pacientes con el mismo número de documento
        Patient.objects.create(**self.data)
        with self.assertRaises(Exception):
            Patient.objects.create(**{**self.data, 'email': 'otro@example.com'})

    def test_str_returns_correct_format(self):
        # La representación en texto debe ser "Apellido, Nombre — Cédula"
        p = Patient.objects.create(**self.data)
        self.assertEqual(str(p), 'García, Ana — 123456789')

    def test_default_is_active_true(self):
        # Por defecto un paciente nuevo está activo
        p = Patient.objects.create(**self.data)
        self.assertTrue(p.is_active)

    def test_document_type_defaults_to_cc(self):
        # El tipo de documento por defecto debe ser CC
        p = Patient.objects.create(**self.data)
        self.assertEqual(p.document_type, 'CC')

    def test_document_type_can_be_changed(self):
        # Se puede cambiar el tipo de documento a CE
        p = Patient.objects.create(**{**self.data, 'document_type': 'CE'})
        self.assertEqual(p.document_type, 'CE')

    def test_occupation_blank_by_default(self):
        # La ocupación debe venir vacía si no se especifica
        p = Patient.objects.create(**self.data)
        self.assertEqual(p.occupation, '')

    def test_occupation_can_be_set(self):
        # Se puede asignar una ocupación al paciente
        p = Patient.objects.create(**{**self.data, 'occupation': 'Ingeniero'})
        self.assertEqual(p.occupation, 'Ingeniero')

    def test_eps_blank_by_default(self):
        # La EPS debe venir vacía si no se especifica
        p = Patient.objects.create(**self.data)
        self.assertEqual(p.eps, '')

    def test_eps_can_be_set(self):
        # Se puede asignar una EPS al paciente
        p = Patient.objects.create(**{**self.data, 'eps': 'SURA'})
        self.assertEqual(p.eps, 'SURA')

    def test_companion_fields_blank_by_default(self):
        # Los campos de acompañante deben venir vacíos por defecto
        p = Patient.objects.create(**self.data)
        self.assertEqual(p.companion_name, '')
        self.assertEqual(p.companion_phone, '')

    def test_companion_fields_can_be_set(self):
        # Se pueden asignar nombre y teléfono del acompañante
        p = Patient.objects.create(**{
            **self.data, 'companion_name': 'María López', 'companion_phone': '3001234567'
        })
        self.assertEqual(p.companion_name, 'María López')
        self.assertEqual(p.companion_phone, '3001234567')


class PatientListViewTest(TestCase):
    # Pruebas sobre la vista que lista los pacientes
    def setUp(self):
        self.patient = Patient.objects.create(
            first_name='Ana', last_name='García', cedula='123456789',
            birth_date='1985-07-22', phone='3001112233',
        )

    def test_list_returns_200(self):
        # La página de lista debe cargar sin errores
        resp = self.client.get(reverse('pacientes:lista'))
        self.assertEqual(resp.status_code, 200)

    def test_list_uses_correct_template(self):
        # La lista debe usar el template correcto
        resp = self.client.get(reverse('pacientes:lista'))
        self.assertTemplateUsed(resp, 'pacientes/lista.html')

    def test_inactive_patient_not_shown_in_list(self):
        # Un paciente desactivado no debe aparecer en la lista
        self.patient.is_active = False
        self.patient.save()
        resp = self.client.get(reverse('pacientes:lista'))
        self.assertNotContains(resp, 'Ana')

    def test_list_shows_only_active_patients(self):
        # Solo deben mostrarse pacientes activos
        Patient.objects.create(first_name='Luis', last_name='Pérez', cedula='987654321', birth_date='1990-01-01')
        self.patient.is_active = False
        self.patient.save()
        resp = self.client.get(reverse('pacientes:lista'))
        self.assertContains(resp, 'Luis')
        self.assertNotContains(resp, 'Ana')


class PatientCreateViewTest(TestCase):
    # Pruebas sobre el formulario de crear paciente
    def test_create_get_returns_200(self):
        # La página de crear debe cargar sin errores
        resp = self.client.get(reverse('pacientes:crear'))
        self.assertEqual(resp.status_code, 200)

    def test_create_post_valid_creates_and_redirects(self):
        # Enviar datos válidos debe crear el paciente y redirigir a la lista
        resp = self.client.post(reverse('pacientes:crear'), {
            'first_name': 'Luis',
            'last_name': 'Martínez',
            'document_type': 'CC',
            'cedula': '987654321',
            'birth_date': '1990-01-15',
            'phone': '3005556677',
            'email': 'luis@example.com',
        })
        self.assertRedirects(resp, reverse('pacientes:lista'))
        self.assertEqual(Patient.objects.count(), 1)

    def test_create_post_invalid_cedula_shows_error(self):
        # Un número de documento muy corto debe mostrar error en el formulario
        resp = self.client.post(reverse('pacientes:crear'), {
            'first_name': 'Luis',
            'last_name': 'Martínez',
            'cedula': '123',
            'birth_date': '1990-01-15',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'debe tener entre 5 y 15 dígitos')

    def test_create_post_missing_required_field_shows_error(self):
        # Si falta un campo obligatorio, el formulario debe mostrar error
        resp = self.client.post(reverse('pacientes:crear'), {
            'first_name': 'Luis',
            'cedula': '987654321',
            'birth_date': '1990-01-15',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Este campo es obligatorio')


class PatientDetailViewTest(TestCase):
    # Pruebas sobre la vista de detalle de un paciente
    def setUp(self):
        self.patient = Patient.objects.create(
            first_name='Ana', last_name='García', cedula='123456789',
            birth_date='1985-07-22',
        )

    def test_detail_active_returns_200(self):
        # Un paciente activo debe mostrar su ficha
        resp = self.client.get(reverse('pacientes:detalle', args=[self.patient.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Ana')

    def test_detail_inactive_returns_404(self):
        # Un paciente inactivo debe dar 404 (como si no existiera)
        self.patient.is_active = False
        self.patient.save()
        resp = self.client.get(reverse('pacientes:detalle', args=[self.patient.pk]))
        self.assertEqual(resp.status_code, 404)

    def test_detail_nonexistent_returns_404(self):
        # Un id que no existe debe dar 404
        resp = self.client.get(reverse('pacientes:detalle', args=[999]))
        self.assertEqual(resp.status_code, 404)


class PatientUpdateViewTest(TestCase):
    # Pruebas sobre la vista de editar paciente
    def setUp(self):
        self.patient = Patient.objects.create(
            first_name='Ana', last_name='García', cedula='123456789',
            birth_date='1985-07-22',
        )

    def test_edit_get_returns_200(self):
        # La página de editar debe cargar sin errores
        resp = self.client.get(reverse('pacientes:editar', args=[self.patient.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_edit_post_valid_updates_and_redirects(self):
        # Enviar datos válidos debe actualizar el paciente y redirigir
        resp = self.client.post(reverse('pacientes:editar', args=[self.patient.pk]), {
            'first_name': 'Ana María',
            'last_name': 'García',
            'document_type': 'CC',
            'cedula': '123456789',
            'birth_date': '1985-07-22',
            'phone': '3001112233',
            'email': 'ana.maria@example.com',
        })
        self.assertRedirects(resp, reverse('pacientes:lista'))
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.first_name, 'Ana María')

    def test_edit_inactive_patient_returns_404(self):
        # Editar un paciente inactivo debe dar 404
        self.patient.is_active = False
        self.patient.save()
        resp = self.client.get(reverse('pacientes:editar', args=[self.patient.pk]))
        self.assertEqual(resp.status_code, 404)


class PatientDeleteViewTest(TestCase):
    # Pruebas sobre la vista de eliminar (soft delete) paciente
    def setUp(self):
        self.patient = Patient.objects.create(
            first_name='Ana', last_name='García', cedula='123456789',
            birth_date='1985-07-22',
        )

    def test_delete_get_returns_confirmation_page(self):
        # La página de confirmación de eliminación debe cargar
        resp = self.client.get(reverse('pacientes:eliminar', args=[self.patient.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '¿Eliminar paciente?')
        self.assertContains(resp, 'Ana')

    def test_delete_post_soft_deletes(self):
        # Al confirmar la eliminación, el paciente se desactiva (no se borra)
        resp = self.client.post(reverse('pacientes:eliminar', args=[self.patient.pk]))
        self.assertRedirects(resp, reverse('pacientes:lista'))
        self.patient.refresh_from_db()
        self.assertFalse(self.patient.is_active)
        self.assertEqual(Patient.objects.count(), 1)

    def test_delete_inactive_patient_returns_404(self):
        # Eliminar un paciente ya inactivo debe dar 404
        self.patient.is_active = False
        self.patient.save()
        resp = self.client.post(reverse('pacientes:eliminar', args=[self.patient.pk]))
        self.assertEqual(resp.status_code, 404)

    def test_delete_preserves_record_in_database(self):
        # El registro del paciente debe seguir existiendo en la base de datos
        pk = self.patient.pk
        self.client.post(reverse('pacientes:eliminar', args=[pk]))
        self.assertTrue(Patient.objects.filter(pk=pk).exists())
        self.assertFalse(Patient.objects.get(pk=pk).is_active)


class PatientSearchTest(TestCase):
    # Pruebas sobre la búsqueda de pacientes
    def setUp(self):
        Patient.objects.create(first_name='Ana', last_name='García', cedula='111111111', birth_date='1985-01-01', phone='3001111111')
        Patient.objects.create(first_name='Carlos', last_name='Pérez', cedula='222222222', birth_date='1990-01-01', phone='3002222222')
        Patient.objects.create(first_name='Ana', last_name='López', cedula='333333333', birth_date='1995-01-01', phone='3003333333')

    def test_search_by_first_name(self):
        # Buscar por nombre debe encontrar los pacientes que coincidan
        resp = self.client.get(reverse('pacientes:lista'), {'q': 'Ana'})
        self.assertEqual(len(resp.context['patients']), 2)

    def test_search_by_last_name(self):
        # Buscar por apellido debe encontrar los pacientes que coincidan
        resp = self.client.get(reverse('pacientes:lista'), {'q': 'Pérez'})
        self.assertEqual(len(resp.context['patients']), 1)

    def test_search_by_cedula(self):
        # Buscar por número de documento debe encontrar al paciente
        resp = self.client.get(reverse('pacientes:lista'), {'q': '222222222'})
        self.assertEqual(len(resp.context['patients']), 1)

    def test_search_by_phone(self):
        # Buscar por teléfono debe encontrar al paciente
        resp = self.client.get(reverse('pacientes:lista'), {'q': '3001111111'})
        self.assertEqual(len(resp.context['patients']), 1)

    def test_search_no_results_returns_empty_list(self):
        # Buscar algo que no existe debe devolver lista vacía
        resp = self.client.get(reverse('pacientes:lista'), {'q': 'Zzzz'})
        self.assertEqual(len(resp.context['patients']), 0)

    def test_search_empty_string_returns_all(self):
        # Buscar sin filtro debe devolver todos los pacientes
        resp = self.client.get(reverse('pacientes:lista'), {'q': ''})
        self.assertEqual(len(resp.context['patients']), 3)


class PatientPaginationTest(TestCase):
    # Pruebas sobre la paginación de la lista
    def setUp(self):
        for i in range(25):
            Patient.objects.create(
                first_name=f'Nombre{i}',
                last_name=f'Apellido{i}',
                cedula=f'{i:09d}',
                birth_date='1990-01-01',
            )

    def test_first_page_has_20_patients(self):
        # La primera página debe mostrar 20 pacientes
        resp = self.client.get(reverse('pacientes:lista'))
        self.assertEqual(len(resp.context['patients']), 20)

    def test_second_page_has_5_patients(self):
        # La segunda página debe mostrar los 5 restantes
        resp = self.client.get(reverse('pacientes:lista'), {'page': 2})
        self.assertEqual(len(resp.context['patients']), 5)

    def test_search_preserves_pagination(self):
        # La paginación debe funcionar también cuando se usa el buscador
        for i in range(25):
            Patient.objects.create(
                first_name=f'Ana{i}',
                last_name=f'López{i}',
                cedula=f'1{i:08d}',
                birth_date='1990-01-01',
            )
        resp = self.client.get(reverse('pacientes:lista'), {'q': 'Nombre', 'page': 1})
        self.assertEqual(len(resp.context['patients']), 20)


class PatientFormTest(TestCase):
    # Pruebas sobre la validación del formulario de pacientes
    def test_form_valid_data_passes_validation(self):
        from pacientes.forms import PatientForm
        form = PatientForm(data={
            'first_name': 'Ana',
            'last_name': 'García',
            'document_type': 'CC',
            'cedula': '123456789',
            'birth_date': '1985-07-22',
            'phone': '3001112233',
            'email': 'ana@example.com',
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_cedula_short(self):
        # Un número de documento muy corto debe hacer que el formulario sea inválido
        from pacientes.forms import PatientForm
        form = PatientForm(data={
            'first_name': 'Ana',
            'last_name': 'García',
            'cedula': '123',
            'birth_date': '1985-07-22',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('cedula', form.errors)

    def test_form_required_fields(self):
        # Si no se envían datos, el formulario debe marcar error en los campos obligatorios
        from pacientes.forms import PatientForm
        form = PatientForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('cedula', form.errors)
        self.assertIn('birth_date', form.errors)
