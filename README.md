# NousData-Lab

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Framework genérico de acceso a datos multi-formato con API REST, servicios de negocio reutilizables y arquitectura extensible.**

[Instalación](#-instalación) · [Características](#-características) · [Arquitectura](#-arquitectura) · [API REST](#-api-rest) · [Ejemplos](#-ejemplos-de-uso)

</div>

---

## 📋 Descripción

**NousData-Lab** es un framework Python profesional que abstrae por completo el acceso a datos, permitiendo trabajar con **5 formatos de persistencia** de forma transparente e intercambiable. Diseñado con patrones de diseño sólidos (Factory, Repository, Strategy), incluye una API REST con autenticación JWT, servicios de negocio para gestión de sesiones/reportes y un sistema de migración entre formatos.

El dominio de ejemplo implementa un **sistema completo de gestión de videojuegos** con juegos, estudios de desarrollo, jugadores, sesiones de juego y géneros.

---

## ✨ Características

| Categoría             | Funcionalidad         | Detalle                                                    |
| --------------------- | --------------------- | ---------------------------------------------------------- |
| 🗄️ **Multi-formato**  | 5 backends de datos   | SQLite · JSON · XML · CSV · TXT (JSON-Lines)               |
| 🔄 **Intercambiable** | Factory + Strategy    | Cambiar formato con un solo parámetro                      |
| 🌐 **API REST**       | Flask + Blueprints    | CRUD completo, paginación, filtros, health check           |
| 🔐 **Autenticación**  | JWT + HMAC-SHA256     | Login, registro, tokens 24h, roles (admin/player/moderator)|
| 🎮 **Sesiones**       | Servicio de negocio   | Compras, tracking de horas, logros, completado, ratings    |
| 📊 **Reportes**       | Motor de informes     | Juegos, sesiones, jugadores, estadísticas, tendencias      |
| 🔀 **Migración**      | Entre formatos        | SQLite → JSON, JSON → XML, etc. con backup automático      |
| ⚙️ **Configuración**  | Deep merge + env vars | JSON config, variables de entorno, validación              |
| 🧬 **Modelos**        | Dataclasses tipadas   | Validación de ratings, contraseñas salted, campos auto     |
| 🏗️ **Extensible**     | Patrón Repository     | Añadir nuevos formatos implementando `DataManager`         |

---

## 🏗 Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                    API REST (Flask)                  │
│        /auth  /games  /sessions  /reports            │
├─────────────────────────────────────────────────────┤
│                 Capa de Negocio                      │
│    AuthService  ·  SessionService  ·  ReportService │
├─────────────────────────────────────────────────────┤
│              Core Framework (Orquesta)               │
│   DataAccessFramework · EntityManager · Repository   │
│        ConfigManager · MigrationManager              │
├─────────────────────────────────────────────────────┤
│              Capa de Acceso a Datos                  │
│  ┌─────────┬──────┬──────┬──────┬─────────────────┐ │
│  │ SQLite  │ JSON │  XML │  CSV │ TXT/JSON-Lines  │ │
│  └─────────┴──────┴──────┴──────┴─────────────────┘ │
└─────────────────────────────────────────────────────┘
```

### Patrones de Diseño

| Patrón         | Uso                                                                          |
| -------------- | ---------------------------------------------------------------------------- |
| **Factory**    | `DataAccessFramework` crea el backend correcto según `data_format`           |
| **Repository** | `EntityManager[T]` proporciona CRUD genérico tipado por entidad              |
| **Strategy**   | Cada `DataManager` implementa la misma interfaz con diferente almacenamiento |

---

## 📁 Estructura del Proyecto

```
NousData-Lab/
├── data_access_framework/         # Paquete principal del framework
│   ├── __init__.py                # API pública, create_framework()
│   ├── models/                    # Entidades del dominio
│   │   └── __init__.py            # Game, Studio, Player, GameSession, Genre
│   ├── core/                      # Motor del framework
│   │   ├── data_access_framework.py   # Orquestador principal
│   │   ├── entity_manager.py      # Repository genérico
│   │   ├── config_manager.py      # Configuración avanzada
│   │   └── migration_manager.py   # Migración entre formatos
│   ├── data_managers/             # Backends de datos
│   │   ├── __init__.py            # DataManager (interfaz base)
│   │   ├── db_manager.py          # SQLite
│   │   ├── json_manager.py        # JSON
│   │   ├── xml_manager.py         # XML (lxml)
│   │   ├── csv_manager.py         # CSV
│   │   └── txt_manager.py         # TXT (JSON-Lines)
│   ├── business/                  # Servicios de negocio
│   │   ├── __init__.py            # Exporta AuthService, SessionService, ReportService
│   │   ├── auth_service.py        # Autenticación JWT + HMAC-SHA256
│   │   ├── session_service.py     # Gestión de sesiones de juego y stats
│   │   └── report_service.py      # Motor de reportes y estadísticas
│   └── api/                       # API REST Flask
│       ├── __init__.py            # create_app()
│       ├── app.py                 # Factory de Flask, JWT middleware
│       └── routes/                # Blueprints
│           ├── auth.py            # POST /auth/login, /auth/register
│           ├── books.py           # CRUD /books
│           ├── loans.py           # /loans endpoints
│           └── reports.py         # /reports endpoints
├── data/                          # Datos persistidos (auto-generado)
├── ejemplo_uso.py                 # Demo completa con todos los servicios
├── demo_simple.py                 # Demo rápida CRUD básico
├── requirements.txt               # Dependencias del proyecto
└── .gitignore
```

---

## 🚀 Instalación

### Requisitos previos

- **Python 3.10+** (recomendado 3.13)
- **pip** (gestor de paquetes)

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/luisrocedev/NousData-Lab.git
cd NousData-Lab

# 2. Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

## 💻 Ejemplos de Uso

### Inicio rápido

```python
from data_access_framework import create_framework
from data_access_framework.models import Book, Author

# Crear framework con SQLite (o 'json', 'xml', 'csv', 'txt')
framework = create_framework(data_format='sqlite')

# Obtener repositorios tipados
book_repo = framework.get_repository('Book')
author_repo = framework.get_repository('Author')

# Crear y guardar un autor
autor = Author(name='Gabriel', last_name='García Márquez', nationality='Colombiano')
author_repo.save(autor)

# Crear y guardar un libro
libro = Book(
    title='Cien años de soledad',
    author_id=autor.id,
    isbn='978-84-376-0494-7',
    genre='Novela',
    pages=417
)
book_repo.save(libro)

# Buscar, listar, eliminar
todos = book_repo.load_all()
encontrado = book_repo.load(libro.id)
book_repo.delete(libro.id)
```

### Servicios de negocio

```python
# Autenticación con JWT
auth = framework.get_service('auth')
user = auth.register_user('Juan', 'Pérez', 'juan@mail.com', 'password123')
token = auth.login('juan@mail.com', 'password123')

# Préstamos
loan_service = framework.get_service('loan')
loan = loan_service.create_loan(user_id=user.id, book_id=libro.id, days=14)
result = loan_service.return_loan(loan.id)

# Reportes
report_service = framework.get_service('report')
report = report_service.generate_books_report()
```

### Migración entre formatos

```python
# Migrar todos los datos de SQLite a JSON con backup
migration = framework.migration_manager
migration.migrate(source_format='sqlite', target_format='json', backup=True)
```

### Cambiar formato de persistencia

```python
# Basta con cambiar un parámetro
framework_json = create_framework(data_format='json')
framework_xml  = create_framework(data_format='xml')
framework_csv  = create_framework(data_format='csv')
framework_txt  = create_framework(data_format='txt')
```

### Ejecutar las demos

```bash
# Demo rápida (CRUD básico)
python demo_simple.py

# Demo completa (auth, préstamos, reportes, API)
python ejemplo_uso.py
```

---

## 🌐 API REST

### Iniciar el servidor

```python
framework = create_framework(data_format='sqlite', config={'api.enabled': True, 'api.port': 5000})
framework.start_api()
# Servidor en http://localhost:5000
```

### Endpoints principales

| Método   | Endpoint             | Auth | Descripción               |
| -------- | -------------------- | ---- | ------------------------- |
| `GET`    | `/health`            | ❌   | Health check del servidor |
| `GET`    | `/stats`             | ❌   | Estadísticas del sistema  |
| `POST`   | `/auth/register`     | ❌   | Registrar usuario         |
| `POST`   | `/auth/login`        | ❌   | Obtener token JWT         |
| `GET`    | `/books`             | ✅   | Listar libros             |
| `POST`   | `/books`             | ✅   | Crear libro               |
| `GET`    | `/books/<id>`        | ✅   | Obtener libro por ID      |
| `PUT`    | `/books/<id>`        | ✅   | Actualizar libro          |
| `DELETE` | `/books/<id>`        | ✅   | Eliminar libro            |
| `POST`   | `/loans`             | ✅   | Crear préstamo            |
| `POST`   | `/loans/<id>/return` | ✅   | Devolver préstamo         |
| `GET`    | `/reports/books`     | ✅   | Reporte de libros         |
| `GET`    | `/reports/loans`     | ✅   | Reporte de préstamos      |

### Ejemplo con cURL

```bash
# Registrar usuario
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Juan","last_name":"Pérez","email":"juan@mail.com","password":"secret123"}'

# Login → obtener token
TOKEN=$(curl -s -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"juan@mail.com","password":"secret123"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

# Crear libro (autenticado)
curl -X POST http://localhost:5000/books \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Mi Libro","isbn":"978-84-376-0494-7","genre":"Ficción","pages":200}'
```

---

## 🔐 Seguridad

- **Contraseñas:** HMAC-SHA256 con salt aleatorio de 16 bytes (`secrets.token_hex`)
- **Tokens JWT:** Expiración configurable (24h por defecto), algoritmo HS256
- **Roles:** Sistema de 3 niveles → `admin`, `librarian`, `user`
- **CORS:** Configurable por entorno

---

## 🛠 Tecnologías

| Componente    | Tecnología                 | Versión |
| ------------- | -------------------------- | ------- |
| Lenguaje      | Python                     | 3.13    |
| API REST      | Flask                      | 2.3+    |
| CORS          | Flask-CORS                 | 4.0+    |
| JWT           | PyJWT / Flask-JWT-Extended | 2.0+    |
| Base de datos | SQLite3 (stdlib)           | —       |
| XML           | lxml                       | 5.0+    |
| Fechas        | python-dateutil            | 2.8+    |

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo `LICENSE` para más detalles.

---

<div align="center">

**NousData-Lab** — Framework de acceso a datos multi-formato

Desarrollado por [Luis Rodriguez Cedeño](https://github.com/luisrocedev)

</div>
