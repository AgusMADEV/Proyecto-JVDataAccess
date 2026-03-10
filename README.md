<div align="center">

# 🎮 NousData-Lab

### Framework genérico de acceso a datos multi-formato
*API REST · Servicios de negocio reutilizables · Arquitectura extensible*

<br>

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3-000000?style=flat-square&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=flat-square&logo=jsonwebtokens&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

<br>

**[Instalación](#-instalación)** • 
**[Características](#-características)** • 
**[Arquitectura](#-arquitectura)** • 
**[API REST](#-api-rest)** • 
**[Ejemplos](#-ejemplos-de-uso)**

</div>

<br>

---

## 💡 Descripción

NousData-Lab es un **framework Python profesional** que abstrae por completo el acceso a datos, permitiendo trabajar con **5 formatos de persistencia** de forma transparente e intercambiable. 

Diseñado con patrones de diseño sólidos (Factory, Repository, Strategy), incluye:
- 🔐 API REST con autenticación JWT
- 💼 Servicios de ne principales

### 🗄️ Multi-formato
Soporta **5 backends de datos**: SQLite · JSON · XML · CSV · TXT (JSON-Lines)

### 🔄 Intercambiable
Cambiar formato con un solo parámetro gracias a Factory + Strategy

### 🌐 API REST completa
Flask + Blueprints con CRUD, paginación, filtros y health check

### 🔐 Autenticación robusta
JWT + HMAC-SHA256 con login, registro, tokens 24h y roles (admin/player/moderator)

### 🎮 Gestión de sesiones
Servicio de negocio para compras, tracking de horas, logros, completado y ratings

### 📊 Motor de reportes
Informes de juegos, sesiones, jugadores, estadísticas y tendencias

### 🔀 Migración de datos
Transforma entre formatos (SQLite → JSON, JSON → XML, etc.) con backup automático

### ⚙️ Configuración avanzada
Deep merge + variables de entorno + validación

### 🧬 Modelos tipados
╔═════════════════════════════════════════════════════╗
║              API REST (Flask)                       ║
║      /auth  /games  /sessions  /reports             ║
╠═════════════════════════════════════════════════════╣
║            Capa de Negocio                          ║
║  AuthService · SessionService · ReportService       ║
╠═════════════════════════════════════════════════════╣
║          Core Framework (Orquesta)                  ║
║  DataAccessFramework · EntityManager · Repository   ║
║     ConfigManager · MigrationManager                ║
╠═════════════════════════════════════════════════════╣
║          Capa de Acceso a Datos                     ║
║  ┌──────┬──────┬──────┬──────┬──────────────────┐  ║
║  │SQLite│ JSON │ XML  │ CSV  │ TXT/JSON-Lines   │  ║
║  └──────┴──────┴──────┴──────┴──────────────────┘  ║
╚═════════════════════════════════════════════════════╝
```

### 🎯 Patrones de Diseño

**Factory Pattern**  
`DataAccessFramework` crea el backend correcto según `data_format`

**Repository Pattern**  
`EntityManager[T]` proporciona CRUD genérico tipado por entidad

**Strategy Pattern**  
Cada `DataManager` implementa la misma interfaz con diferente almacenamiento

<br>      ConfigManager · MigrationManager              │
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
│   │   └── re
- Python 3.10+ (recomendado 3.13)
- pip (gestor de paquetes)

### Pasos de instalación

```bash
# Clonar el repositorio
git clone https://github.com/AgusMADEV/NousData-Lab.git
cd NousData-Lab

# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

<br> Requisitos previos

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

---uso

### 🚀💻 Ejemplos de Uso

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
```💼 

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
🔄 
```python
# Migrar todos los datos de SQLite a JSON con backup
migration = framework.migration_manager
migration.migrate(source_format='sqlite', target_format='json', backup=True)
```

### ⚙️ Cambiar formato de persistencia

```python
# Basta con cambiar un parámetro
framework_json = create_framework(data_format='json')
framework_xml  = create_framework(data_format='xml')
framework_csv  = create_framework(data_format='csv')
framework_txt  = create_framework(data_format='txt')
```

### 🎯 Ejecutar las demos

```bash
# Demo rápida (CRUD básico)
python demo_simple.py

# Demo completa (auth, préstamos, reportes, API)
python ejemplo_uso.py
```

---

## 🌐 API REST

### 🔧 Iniciar el servidor

```python
framework = create_framework(data_format='sqlite', config={'api.enabled': True, 'api.port': 5000})
framework.start_api()
# Servidor en http://localhost:5000
```

### 📍 Endpoints principales

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

### 🔨 Ejemplo con cURL

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

> **Contraseñas**  
> HMAC-SHA256 con salt aleatorio de 16 bytes (`secrets.token_hex`)

> **Tokens JWT**  
> Expiración configurable (24h por defecto), algoritmo HS256

> **Roles**  
> SistStack tecnológico

<table>
<tr>
<td><strong>Lenguaje</strong></td>
<td>Python 3.13</td>
</tr>
<tr>
<td><strong>API REST</strong></td>
<td>Flask 2.3+</td>
</tr>
<tr>
<td><strong>CORS</strong></td>
<td>Flask-CORS 4.0+</td>
</tr>
<tr>
<td><strong>JWT</strong></td>
<td>PyJWT / Flask-JWT-Extended 2.0+</td>
</tr>
<tr>
<td><strong>Base de datos</strong></td>
<td>SQLite3 (stdlib)</td>
### 🎮 NousData-Lab
*Framework de acceso a datos multi-formato*

<br>

Desarrollado con ❤️ por [Agustín Morcillo](https://github.com/AgusMADEV)

[![GitHub](https://img.shields.io/badge/GitHub-AgusMADEV-181717?style=flat-square&logo=github)](https://github.com/AgusMADEV
<td>lxml 5.0+</td>
</tr>
<tr>
<td><strong>Fechas</strong></td>
<td>python-dateutil 2.8+</td>
</tr>
</table>

<br>PI REST      | Flask                      | 2.3+    |
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
