# CoderBlog 🚀 | Trabajo Práctico Final - Python

![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1+-092E20?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3+-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

Proyecto final desarrollado para el curso de **Python** en **Coderhouse**. Se trata de una plataforma web de Blog completamente funcional, modular y consolidada, construida con el framework **Django** y estilizada de manera moderna y responsiva con **Bootstrap 5**.

---

## 📌 Funcionalidades Principales

### 1. Gestión Integral de Publicaciones (CRUD Web)
- **Listado de Posts:** Vista principal pública con tarjetas de artículos, autor, fecha y vista previa.
- **Detalle de Post:** Lectura completa con imagen destacada en alta resolución, autoría y fecha de publicación/edición.
- **Creación de Posts:** Formulario protegido para redactar artículos con título, subtítulo, cuerpo y carga de imágenes.
- **Edición y Eliminación:** Control granular de permisos; únicamente el autor de la publicación o un superusuario tienen privilegios para editar o eliminar sus artículos.
- **Manejo Seguro de Imágenes:** Implementación defensiva de plantillas: si un artículo no posee imagen, el diseño utiliza fallbacks limpios sin romperse ni generar excepciones.

### 2. Autenticación y Perfiles de Usuario
- **Registro de Usuarios:** Formulario con validaciones seguras integradas de Django.
- **Inicio y Cierre de Sesión:** Manejo de sesiones de usuario con alertas informativas (flash messages).
- **Distinción de Visitantes:** La barra de navegación se adapta dinámicamente según si el visitante es un usuario anónimo o un autor autenticado.
- **Perfil de Usuario:** Cada usuario dispone de su página de perfil con avatar personalizado, biografía, enlace a redes o sitio web, y el listado de todos sus artículos publicados.
- **Edición de Perfil y Cambio de Contraseña:** Vistas protegidas para actualizar tanto datos de la cuenta como del perfil público.

### 3. Rutas Protegidas y Seguridad
- Implementación de `LoginRequiredMixin` y `UserPassesTestMixin` a nivel de vistas del servidor (la seguridad no depende solo de ocultar botones en el HTML).
- Redirección automática al inicio de sesión ante intentos de acceso no autorizado.
- Protección nativa contra vulnerabilidades CSRF, SQL Injection y XSS provista por Django.

### 4. Motor de Búsqueda
- Buscador integrado en la cabecera que filtra publicaciones en tiempo real por coincidencia en título, subtítulo o contenido, notificando cuando no se encuentran resultados.

### 5. Sección "Acerca de Mí"
- Página informativa con la presentación del autor, contexto del proyecto y detalle de la arquitectura técnica utilizada.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** [Python 3.14+](https://www.python.org/)
- **Framework Web:** [Django 6.1+](https://www.djangoproject.com/)
- **Frontend / Estilos:** [Bootstrap 5.3](https://getbootstrap.com/) y [Bootstrap Icons](https://icons.getbootstrap.com/)
- **Gestión y Procesamiento de Imágenes:** [Pillow 13.0+](https://python-pillow.org/)
- **Base de Datos:** SQLite 3 (integrada por defecto con Django ORM)
- **Control de Versiones:** Git y GitHub

---

## 📂 Estructura del Proyecto

```text
coderhouse-python-tp-final/
├── accounts/                  # App de autenticación y gestión de perfiles
│   ├── migrations/            # Historial de migraciones de base de datos
│   ├── forms.py               # Formularios de registro, edición de perfil y usuario
│   ├── models.py              # Modelo Perfil (OneToOne con User, avatar, bio)
│   ├── tests.py               # Tests unitarios de autenticación y perfiles
│   ├── urls.py                # Rutas: login, logout, registro, perfil, editar
│   └── views.py               # Vistas basadas en clases y control de acceso
├── blog/                      # App principal del Blog
│   ├── management/            # Comandos personalizados de Django (poblar_datos)
│   ├── migrations/            # Historial de migraciones de Post
│   ├── forms.py               # Formulario de creación y edición de posts
│   ├── models.py              # Modelo Post (título, subtítulo, contenido, imagen, autor)
│   ├── tests.py               # Tests de CRUD, búsqueda y rutas protegidas
│   ├── urls.py                # Rutas del CRUD de posts y About
│   └── views.py               # Class-Based Views (List, Detail, Create, Update, Delete)
├── blog_project/              # Módulo de configuración principal
│   ├── settings.py            # Configuración de apps, media, estáticos y templates
│   ├── urls.py                # Enrutador general y servicio de media en DEBUG
│   └── wsgi.py
├── media/                     # Directorio de subida de imágenes (posts y avatares)
├── static/                    # Archivos estáticos propios (CSS, SVG placeholders)
├── templates/                 # Plantillas HTML con Bootstrap 5
│   ├── base.html              # Plantilla base con navbar y footer responsivos
│   ├── accounts/              # Templates de login, registro, perfil y edición
│   └── blog/                  # Templates de listado, detalle, formulario y borrado
├── .env.example               # Ejemplo de variables de entorno
├── .gitignore                 # Configuración de exclusiones Git profesional
├── manage.py                  # Script de gestión de Django
├── README.md                  # Documentación del proyecto
└── requirements.txt           # Lista de dependencias del proyecto
```

---

## 🚀 Guía de Instalación y Ejecución Local

Para clonar, instalar y poner en marcha el proyecto en cualquier computadora, sigue estos sencillos pasos:

### 1. Clonar el repositorio
```bash
git clone https://github.com/mateo-calvo/coderhouse-python-tp-final.git
cd coderhouse-python-tp-final
```

### 2. Crear y activar el entorno virtual

- **En Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

- **En macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar las dependencias
Con el entorno virtual activo, instala los paquetes requeridos:
```bash
pip install -r requirements.txt
```

### 4. Ejecutar las migraciones
Prepara la base de datos aplicando todas las migraciones del sistema:
```bash
python manage.py migrate
```

### 5. Cargar datos de demostración (Opcional pero Recomendado)
El proyecto incluye un comando personalizado que crea automáticamente usuarios y artículos de prueba para una revisión inmediata:
```bash
python manage.py poblar_datos
```
> **Credenciales generadas por el comando:**
> - **Superusuario / Admin:** Usuario: `admin` | Contraseña: `admin123`
> - **Usuario Autor:** Usuario: `mateo` | Contraseña: `coder123`

*(Alternativamente, puedes crear tu propio superusuario manualmente con `python manage.py createsuperuser`)*.

### 6. Iniciar el servidor de desarrollo
```bash
python manage.py runserver
```

Abre tu navegador web e ingresa a:  
👉 **`http://127.0.0.1:8000/`**

---

## 🧪 Ejecución de Tests Automatizados

El proyecto cuenta con una suite completa de pruebas unitarias que verifican el correcto funcionamiento de los modelos, las rutas protegidas, la autenticación y la búsqueda:

```bash
python manage.py test
```

---

## 👤 Autor

- **Nombre:** Mateo Calvo
- **Curso:** Python - Coderhouse
- **GitHub:** [@mateo-calvo](https://github.com/mateo-calvo)
- **Email:** mateocalvo1706@gmail.com

---

## 📄 Licencia

Este proyecto fue desarrollado con fines educativos como entrega final para Coderhouse. Código libre para consulta y aprendizaje.
