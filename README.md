# dentalPro
 DentalPro es un software de gestión odontológica 100% offline que se instala en tu computador. Sin suscripciones, sin internet requerido. Fichas digitales, odontograma interactivo, citas, inventario y facturación DIAN integrada. Hecho en Colombia para consultorios independientes.
# DentalPro
> Software de gestión odontológica local. Offline-first. Hecho en Colombia para consultorios independientes.

---

## 📖 ¿Qué es DentalPro?
DentalPro es un sistema clínico completo que se instala directamente en tu computador. **No requiere internet para funcionar**, no cobra suscripciones mensuales y guarda toda la información de tu consultorio de forma local y segura. 

Está diseñado para que el odontólogo pierda menos tiempo en papeleo y más tiempo atendiendo. El sistema traduce automáticamente términos técnicos a un lenguaje claro que el paciente entiende al instante.

---

## ✨ Características Principales
| Función | Qué hace | Para qué sirve |
|---|---|---|
| 🖥️ **100% Local** | Funciona sin conexión a internet | Evita caídas de red y protege la privacidad |
| 🦷 **Odontograma SVG** | Gráfico interactivo de los 32 dientes | Marca estados con un clic, sin dibujos manuales |
| 📋 **Historia Clínica** | Registro digital + traducción a lenguaje humano | El paciente entiende su diagnóstico sin googlear |
| 🔍 **Búsqueda Instantánea** | Filtra por nombre, cédula o teléfono sin recargar | Encuentra cualquier ficha en menos de 1 segundo |
| 📅 **Gestión de Citas** | Calendario, estados y recordatorios | Reduce ausencias y organiza la jornada |
| 📦 **Inventario** | Control de materiales con alertas de stock mínimo | Nunca te quedas sin insumos a mitad de procedimiento |
| 💰 **Finanzas & DIAN** | Facturación interna y exportación de datos | Cumple con reportes tributarios sin software extra |
| 🤖 **Asistente IA** *(Opcional)* | Interpretación de notas y resúmenes clínicos | Solo se activa si hay internet. Tus datos no se guardan en la nube |

---

## 🛠️ Stack Tecnológico (y por qué lo usamos)
| Tecnología | Rol en el proyecto | Explicación sencilla |
|---|---|---|
| **Django 4.2** | Motor principal | Organiza datos, usuarios y seguridad de forma probada y estable |
| **SQLite** | Base de datos | Archivo local `.sqlite3`. No requiere instalación ni servidores |
| **HTMX 1.9** | Interfaz dinámica | Hace que los botones y formularios respondan al instante sin JavaScript complejo |
| **Tailwind CSS 3** | Diseño visual | Estilo moderno, limpio y adaptable a cualquier pantalla |
| **Python 3.11** | Lenguaje base | Rápido, legible y con librerías maduras para escritorio |
| **PyInstaller** | Empaquetado final | Convierte el código en un `.exe` instalable en Windows |

---

## 🚀 Instalación

### 👨‍💻 Para desarrolladores (entorno de pruebas)
```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/dentalpro.git
cd dentalpro

# 2. Crear entorno aislado
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac / Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Preparar base de datos y crear usuario administrador
python manage.py migrate --settings=config.settings.dev
python manage.py createsuperuser --settings=config.settings.dev

# 5. Iniciar servidor local
python manage.py runserver --settings=config.settings.dev
```
🌐 Abre `http://127.0.0.1:8000` en tu navegador.

### 💼 Para consultorios (instalador final)
*Disponible al completar la Fase 13.* Se entregará un archivo `DentalPro_Setup.exe` que instala la aplicación, crea la base de datos automáticamente y abre el programa al hacer doble clic. No se requiere Python ni conocimientos técnicos.

---

## 📁 Estructura del Proyecto
```
dentalpro/
├── config/           # Ajustes generales, rutas y seguridad
├── core/             # Plantillas base, estilos comunes y utilidades
├── pacientes/        # Fichas, historia clínica y odontograma
├── citas/            # Calendario y recordatorios
├── inventario/       # Control de materiales y alertas
├── finanzas/         # Facturación y exportación DIAN
├── media/            # Radiografías y fotos clínicas (almacenamiento local)
├── templates/        # Interfaz visual (HTML + Tailwind + HTMX)
└── db.sqlite3        # Base de datos local (se crea sola)
```
C
