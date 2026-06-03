import datetime
from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from pacientes.models import Patient


class PatientModelTest(TestCase):
    def setUp(self):
        self.data = {
            'first_name': 'Ana',
            'last_name': 'García',
            'cedula': '123456789',
            'birth_date': datetime.date(1985, 7, 22),
            'phone': '3001112233',
            'email': 'ana@example.com',
            'blood_type': 'O+',
        }

    def test_create_valid_patient(self):
        p = Patient.objects.create(**self.data)
        self.assertEqual(Patient.objects.count(), 1)
        self.assertTrue(p.is_active)

    def test_cedula_less_than_6_digits_fails(self):
        p = Patient(**{**self.data, 'cedula': '12345'})
        with self.assertRaises(ValidationError):
            p.full_clean()

    def test_cedula_more_than_10_digits_fails(self):
        p = Patient(**{**self.data, 'cedula': '12345678901'})
        with self.assertRaises(ValidationError):
            p.full_clean()

    def test_cedula_duplicate_fails(self):
        Patient.objects.create(**self.data)
        with self.assertRaises(Exception):
            Patient.objects.create(**{**self.data, 'email': 'otro@example.com'})

    def test_str_returns_correct_format(self):
        p = Patient.objects.create(**self.data)
        self.assertEqual(str(p), 'García, Ana — 123456789')

    def test_default_is_active_true(self):
        p = Patient.objects.create(**self.data)
        self.assertTrue(p.is_active)


class PatientListViewTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            first_name='Ana', last_name='García', cedula='123456789',
            birth_date='1985-07-22', phone='3001112233',
        )

    def test_list_returns_200(self):
        resp = self.client.get(reverse('pacientes:lista'))
        self.assertEqual(resp.status_code, 200)

    def test_list_uses_correct_template(self):
        resp = self.client.get(reverse('pacientes:lista'))
        self.assertTemplateUsed(resp, 'pacientes/lista.html')

    def test_inactive_patient_not_shown_in_list(self):
        self.patient.is_active = False
        self.patient.save()
        resp = self.client.get(reverse('pacientes:lista'))
        self.assertNotContains(resp, 'Ana')

    def test_list_shows_only_active_patients(self):
        Patient.objects.create(first_name='Luis', last_name='Pérez', cedula='987654321', birth_date='1990-01-01')
        self.patient.is_active = False
        self.patient.save()
        resp = self.client.get(reverse('pacientes:lista'))
        self.assertContains(resp, 'Luis')
        self.assertNotContains(resp, 'Ana')


class PatientCreateViewTest(TestCase):
    def test_create_get_returns_200(self):
        resp = self.client.get(reverse('pacientes:crear'))
        self.assertEqual(resp.status_code, 200)

    def test_create_post_valid_creates_and_redirects(self):
        resp = self.client.post(reverse('pacientes:crear'), {
            'first_name': 'Luis',
            'last_name': 'Martínez',
            'cedula': '987654321',
            'birth_date': '1990-01-15',
            'phone': '3005556677',
            'email': 'luis@example.com',
        })
        self.assertRedirects(resp, reverse('pacientes:lista'))
        self.assertEqual(Patient.objects.count(), 1)

    def test_create_post_invalid_cedula_shows_error(self):
        resp = self.client.post(reverse('pacientes:crear'), {
            'first_name': 'Luis',
            'last_name': 'Martínez',
            'cedula': '123',
            'birth_date': '1990-01-15',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'debe tener entre 6 y 10 dígitos')

    def test_create_post_missing_required_field_shows_error(self):
        resp = self.client.post(reverse('pacientes:crear'), {
            'first_name': 'Luis',
            'cedula': '987654321',
            'birth_date': '1990-01-15',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Este campo es obligatorio')


class PatientDetailViewTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            first_name='Ana', last_name='García', cedula='123456789',
            birth_date='1985-07-22',
        )

    def test_detail_active_returns_200(self):
        resp = self.client.get(reverse('pacientes:detalle', args=[self.patient.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Ana')

    def test_detail_inactive_returns_404(self):
        self.patient.is_active = False
        self.patient.save()
        resp = self.client.get(reverse('pacientes:detalle', args=[self.patient.pk]))
        self.assertEqual(resp.status_code, 404)

    def test_detail_nonexistent_returns_404(self):
        resp = self.client.get(reverse('pacientes:detalle', args=[999]))
        self.assertEqual(resp.status_code, 404)


class PatientUpdateViewTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            first_name='Ana', last_name='García', cedula='123456789',
            birth_date='1985-07-22',
        )

    def test_edit_get_returns_200(self):
        resp = self.client.get(reverse('pacientes:editar', args=[self.patient.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_edit_post_valid_updates_and_redirects(self):
        resp = self.client.post(reverse('pacientes:editar', args=[self.patient.pk]), {
            'first_name': 'Ana María',
            'last_name': 'García',
            'cedula': '123456789',
            'birth_date': '1985-07-22',
            'phone': '3001112233',
            'email': 'ana.maria@example.com',
        })
        self.assertRedirects(resp, reverse('pacientes:lista'))
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.first_name, 'Ana María')

    def test_edit_inactive_patient_returns_404(self):
        self.patient.is_active = False
        self.patient.save()
        resp = self.client.get(reverse('pacientes:editar', args=[self.patient.pk]))
        self.assertEqual(resp.status_code, 404)


class PatientDeleteViewTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            first_name='Ana', last_name='García', cedula='123456789',
            birth_date='1985-07-22',
        )

    def test_delete_get_returns_confirmation_page(self):
        resp = self.client.get(reverse('pacientes:eliminar', args=[self.patient.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '¿Eliminar paciente?')
        self.assertContains(resp, 'Ana')

    def test_delete_post_soft_deletes(self):
        resp = self.client.post(reverse('pacientes:eliminar', args=[self.patient.pk]))
        self.assertRedirects(resp, reverse('pacientes:lista'))
        self.patient.refresh_from_db()
        self.assertFalse(self.patient.is_active)
        self.assertEqual(Patient.objects.count(), 1)

    def test_delete_inactive_patient_returns_404(self):
        self.patient.is_active = False
        self.patient.save()
        resp = self.client.post(reverse('pacientes:eliminar', args=[self.patient.pk]))
        self.assertEqual(resp.status_code, 404)

    def test_delete_preserves_record_in_database(self):
        pk = self.patient.pk
        self.client.post(reverse('pacientes:eliminar', args=[pk]))
        self.assertTrue(Patient.objects.filter(pk=pk).exists())
        self.assertFalse(Patient.objects.get(pk=pk).is_active)


class PatientSearchTest(TestCase):
    def setUp(self):
        Patient.objects.create(first_name='Ana', last_name='García', cedula='111111111', birth_date='1985-01-01', phone='3001111111')
        Patient.objects.create(first_name='Carlos', last_name='Pérez', cedula='222222222', birth_date='1990-01-01', phone='3002222222')
        Patient.objects.create(first_name='Ana', last_name='López', cedula='333333333', birth_date='1995-01-01', phone='3003333333')

    def test_search_by_first_name(self):
        resp = self.client.get(reverse('pacientes:lista'), {'q': 'Ana'})
        self.assertEqual(len(resp.context['patients']), 2)

    def test_search_by_last_name(self):
        resp = self.client.get(reverse('pacientes:lista'), {'q': 'Pérez'})
        self.assertEqual(len(resp.context['patients']), 1)

    def test_search_by_cedula(self):
        resp = self.client.get(reverse('pacientes:lista'), {'q': '222222222'})
        self.assertEqual(len(resp.context['patients']), 1)

    def test_search_by_phone(self):
        resp = self.client.get(reverse('pacientes:lista'), {'q': '3001111111'})
        self.assertEqual(len(resp.context['patients']), 1)

    def test_search_no_results_returns_empty_list(self):
        resp = self.client.get(reverse('pacientes:lista'), {'q': 'Zzzz'})
        self.assertEqual(len(resp.context['patients']), 0)

    def test_search_empty_string_returns_all(self):
        resp = self.client.get(reverse('pacientes:lista'), {'q': ''})
        self.assertEqual(len(resp.context['patients']), 3)


class PatientPaginationTest(TestCase):
    def setUp(self):
        for i in range(25):
            Patient.objects.create(
                first_name=f'Nombre{i}',
                last_name=f'Apellido{i}',
                cedula=f'{i:09d}',
                birth_date='1990-01-01',
            )

    def test_first_page_has_20_patients(self):
        resp = self.client.get(reverse('pacientes:lista'))
        self.assertEqual(len(resp.context['patients']), 20)

    def test_second_page_has_5_patients(self):
        resp = self.client.get(reverse('pacientes:lista'), {'page': 2})
        self.assertEqual(len(resp.context['patients']), 5)

    def test_search_preserves_pagination(self):
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
    def test_form_valid_data_passes_validation(self):
        from pacientes.forms import PatientForm
        form = PatientForm(data={
            'first_name': 'Ana',
            'last_name': 'García',
            'cedula': '123456789',
            'birth_date': '1985-07-22',
            'phone': '3001112233',
            'email': 'ana@example.com',
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_cedula_short(self):
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
        from pacientes.forms import PatientForm
        form = PatientForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('cedula', form.errors)
        self.assertIn('birth_date', form.errors)
