# Auditoría DentalPro — para el aprendiz

## ¿Por qué esto?
Hice una revisión del código para encontrar cosas que corregir y para definir qué falta para que el módulo **Pacientes** esté completo. Acá te explico todo claro.

---

## 1. Cosas que están bien ✅

- El modelo `Patient` está bien estructurado
- El CRUD (Crear, Leer, Actualizar, Eliminar) funciona completo
- El **soft delete** (marcar como inactivo en vez de borrar) está bien implementado
- Los tests están completos y pasan
- La búsqueda por nombre, cédula y teléfono funciona
- Los templates se ven bonitos con Tailwind
- La paginación funciona

---

## 2. Cosas que corregir (importantes) ⚠️

### 2.1 README dice Django 4.2 pero estás usando Django 5.2
- **Qué hacer**: En el README, cambiar `Django 4.2` por `Django 5.2`
- **Por qué**: El `requirements.txt` ya tiene `django~=5.2.0` y las migraciones se generaron con Django 5.2.15. El README debe reflejar la realidad o alguien se confunde.

### 2.2 README dice que existen módulos que no has creado
Dice que hay `citas/`, `inventario/`, `finanzas/`, `media/` pero solo tienes `pacientes/` y `core/`.
- **Qué hacer**: En el README, aclarar que esos módulos son **a futuro** (planes)
- **Por qué**: Si alguien lee el README y va a buscar esas carpetas, va a pensar que el proyecto está incompleto o roto

### 2.3 La SECRET_KEY está visible en GitHub
- **Qué hacer**: Usar una variable de entorno
- **Por qué**: Si alguien clona tu repo, tiene tu clave secreta. Con ella pueden firmar cookies falsas y suplantar usuarios. Es un riesgo de seguridad
- **Cómo se hace**:
  ```python
  import os
  SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'clave-temporal-solo-para-desarrollo')
  ```

### 2.4 DEBUG = True fijo
- **Qué hacer**: Que DEBUG se active solo si no está en producción
- **Por qué**: Si alguna vez pones esto en un servidor, con DEBUG=True la gente puede ver errores con información sensible de tu base de datos
- **Cómo se hace**:
  ```python
  DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
  ```

### 2.5 Tailwind y HTMX desde CDN (contradice "offline-first")
El README dice que es **offline-first** pero Tailwind y HTMX se cargan desde internet.
- **Qué hacer**: Descargar los archivos CSS/JS y ponerlos en una carpeta `static/`, luego cargarlos desde ahí
- **Por qué**: Si el consultorio no tiene internet, la interfaz se ve fea (sin estilos) y el HTMX no funciona

### 2.6 No existe la carpeta `static/` aunque está configurada
- **Qué hacer**: Crear `static/` con un archivo `.gitkeep`
- **Por qué**: Django la tiene configurada en settings.py, si no existe puede dar error al hacer `collectstatic`

### 2.7 Archivo `bitacora` suelto en la raíz
- **Qué hacer**: Borrarlo o moverlo a otro lado
- **Por qué**: No es parte del proyecto, solo tiene la palabra "auditoria" adentro

---

## 3. Lo que falta para que Pacientes esté completo

Tienes el CRUD básico, pero para un consultorio odontológico real hacen falta estos campos:

### 3.1 Tipo de documento
- **Ejemplos**: CC (cédula), CE (extranjería), NIT, Pasaporte
- **Por qué**: No todos los pacientes tienen cédula colombiana
- **Cómo**: Un `CharField` con `choices`

### 3.2 Ocupación
- **Por qué**: Sirve para la historia clínica y estadísticas
- **Cómo**: Un `CharField` opcional

### 3.3 EPS / Régimen de salud
- **Por qué**: En Colombia es obligatorio para facturación y remisiones
- **Cómo**: Un `CharField` opcional

### 3.4 Nombre y teléfono del acompañante
- **Por qué**: Para contactar a alguien si el paciente no responde o es menor de edad
- **Cómo**: Dos campos opcionales

### 3.5 Validación de cédula más flexible
- **Qué hacer**: Cambiar el validador de `^\d{6,10}$` a `^\d{5,15}$`
- **Por qué**: Hay cédulas de más de 10 dígitos (con dígito de verificación) y el NIT puede tener más
- **Cómo**: Solo cambiar el regex en `models.py`

### 3.6 Mensajes de éxito al guardar
- **Qué hacer**: Mostrar "Paciente creado correctamente" después de cada acción
- **Por qué**: El usuario necesita saber si la operación funcionó o no
- **Cómo**: Usar `messages.success(request, 'Paciente creado exitosamente')` en las vistas y mostrar los mensajes en `base.html`

---

## Tips para que le expliques

1. **Una cosa a la vez** — cada commit debe hacer solo UN cambio. Así si algo se daña, sabes exactamente qué lo causó
2. **Commits descriptivos** — en lugar de "arreglos varios", usa "fix: actualiza versión Django en README" o "feat: agrega campo ocupación a paciente"
3. **Siempre en rama** — nunca trabajes directo en `main`. Crea una rama `mejora-pacientes`, trabaja ahí, y cuando esté lista haces merge
4. **Prueba antes de subir** — corre `python manage.py test` antes de hacer commit
5. **Pregunta si no entiendes** — es mejor preguntar que adivinar y romper algo
