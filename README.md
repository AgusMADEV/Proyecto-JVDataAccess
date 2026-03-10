<div align="center">

# 🎮 JVDATAACCESS

### Framework de Gestión de Videojuegos Multi-Formato
*Acceso a datos transparente · Servicios de negocio · API REST*

<br>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3+-000000?style=flat-square&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=flat-square&logo=jsonwebtokens&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

<br>

**[Instalación](#-instalación)** • 
**[Características](#-características)** • 
**[Modelos](#-modelos-de-datos)** • 
**[API](#-api-rest)** • 
**[Uso](#-ejemplos-de-uso)**

</div>

<br>

---

## 💡 Descripción

**JVDATAACCESS** es un framework Python para la gestión de videojuegos que proporciona abstracción completa del almacenamiento de datos. Diseñado con patrones de diseño profesionales (Factory, Repository, Strategy), permite cambiar entre **5 formatos de persistencia** sin modificar el código de tu aplicación.

El framework incluye:
- 🎮 **Sistema completo de videojuegos**: juegos, estudios, jugadores, géneros y sesiones
- 🔐 **Autenticación segura**: Registro y login con HMAC-SHA256
- 🎯 **Servicios de negocio**: Gestión de sesiones de juego, compras y logros
- 🌐 **API REST**: Endpoints completos con Flask y JWT
- 💾 **Multi-formato**: SQLite, JSON, XML, CSV, TXT intercambiables

<br>

---

## ✨ Características

### 💾 Persistencia Multi-Formato
Cambia entre **5 backends** sin modificar tu código:
- **SQLite** - Base de datos relacional embebida
- **JSON** - Archivos JSON estructurados
- **XML** - Formato XML con lxml
- **CSV** - Archivos CSV tabulares
- **TXT** - JSON Lines (un objeto por línea)

### 🎮 Dominio de Videojuegos
Sistema completo con:
- **Juegos**: Título, plataforma, género, rating (0-10), precio, horas de juego
- **Estudios**: Desarrolladores con año de fundación, país, descripción
- **Jugadores**: Usuarios con niveles, horas totales de juego, roles (player/admin/moderator)
- **Sesiones**: Tracking de compras, horas jugadas, logros, completado
- **Géneros**: Categorías de juegos con jerarquía opcional

### 🔐 Autenticación Robusta
- Hash de contraseñas con **HMAC-SHA256** y sal aleatoria de 16 bytes
- Sistema de **roles** (player, admin, moderator)
- Login con validación de email
- Gestión de usuarios activos/inactivos

### 💼 Servicios de Negocio

**GameSessionService**
- Crear sesiones de juego (compras)
- Registrar horas jugadas
- Marcar juegos como completados
- Sistema de logros
- Estadísticas de jugador

**AuthService**
- Registro de jugadores
- Autenticación segura
- Validación de credenciales
- Gestión de permisos

### 🌐 API REST con Flask
- Endpoints CRUD para juegos
- Autenticación con JWT
- Gestión de sesiones de juego
- Sistema de roles y permisos

### 🏗️ Arquitectura Profesional
- **Factory Pattern**: Creación dinámica del backend
- **Repository Pattern**: Interfaz unificada CRUD
- **Strategy Pattern**: Implementaciones intercambiables
- **Dependency Injection**: Servicios desacoplados

<br>

---

## 🗂 Modelos de Datos

### Game (Videojuego)
```python
Game(
    title: str,              # Título del juego
    studio_id: str,          # ID del estudio desarrollador
    platform: str,           # PC, PlayStation, Xbox, Nintendo Switch, Mobile
    genre: str,              # Género del juego
    release_year: int,       # Año de lanzamiento (1970-presente)
    rating: float,           # Calificación 0-10
    price: float,            # Precio en €
    playtime_hours: int,     # Horas para completar
    multiplayer: bool,       # ¿Tiene modo multijugador?
    available: bool          # ¿Disponible para compra?
)
```

### Studio (Estudio de Desarrollo)
```python
Studio(
    name: str,               # Nombre del estudio
    founded_year: int,       # Año de fundación (1950-presente)
    country: str,            # País de origen
    website: str,            # URL del sitio web
    description: str         # Descripción del estudio
)
```

### Player (Jugador)
```python
Player(
    username: str,           # Nombre de usuario único
    email: str,              # Email válido
    password_hash: str,      # Hash HMAC-SHA256 con sal
    role: str,               # player, admin, moderator
    active: bool,            # ¿Usuario activo?
    level: int,              # Nivel del jugador (1+)
    total_playtime_hours: float  # Horas totales de juego
)
```

### GameSession (Sesión de Juego)
```python
GameSession(
    player_id: str,          # ID del jugador
    game_id: str,            # ID del juego
    purchase_date: datetime, # Fecha de compra
    hours_played: float,     # Horas jugadas
    completed: bool,         # ¿Juego completado?
    achievements: int,       # Número de logros
    last_played: datetime    # Última vez jugado
)
```

### Genre (Género)
```python
Genre(
    name: str,               # Nombre del género
    description: str,        # Descripción
    parent_id: str           # ID del género padre (jerarquía)
)
```

<br>

---

## 🏗 Arquitectura

```
╔═════════════════════════════════════════════════════╗
║         API REST (Flask + JWT)                      ║
║    /auth/login  /games  /sessions                   ║
╠═════════════════════════════════════════════════════╣
║           Servicios de Negocio                      ║
║    AuthService  ·  GameSessionService               ║
╠═════════════════════════════════════════════════════╣
║          Core del Framework                         ║
║  DataAccessFramework · EntityManager · Repository   ║
║          ConfigManager · Factory                    ║
╠═════════════════════════════════════════════════════╣
║         Gestores de Datos (Strategy)                ║
║  ┌──────┬──────┬──────┬──────┬──────────────────┐  ║
║  │SQLite│ JSON │ XML  │ CSV  │ TXT (JSON-Lines) │  ║
║  └──────┴──────┴──────┴──────┴──────────────────┘  ║
╠═════════════════════════════════════════════════════╣
║              Modelos de Datos                       ║
║   Game · Studio · Player · GameSession · Genre      ║
╚═════════════════════════════════════════════════════╝
```

<br>

---

## 📁 Estructura del Proyecto

```
JVDATAACCESS/
├── data_access_framework/           # 📦 Paquete principal
│   ├── __init__.py                  # API pública: create_framework()
│   │
│   ├── models/                      # 🎯 Modelos de dominio
│   │   └── __init__.py              # Game, Studio, Player, GameSession, Genre
│   │
│   ├── core/                        # ⚙️ Motor del framework
│   │   ├── data_access_framework.py # Orquestador principal (Factory)
│   │   ├── entity_manager.py        # Repository genérico tipado
│   │   └── config_manager.py        # Configuración y logging
│   │
│   ├── data_managers/               # 💾 Backends de persistencia
│   │   ├── __init__.py              # Interfaz DataManager
│   │   ├── db_manager.py            # SQLite (SQLAlchemy)
│   │   ├── json_manager.py          # JSON con validación
│   │   ├── xml_manager.py           # XML (lxml)
│   │   ├── csv_manager.py           # CSV con pandas
│   │   └── txt_manager.py           # TXT (JSON Lines)
│   │
│   ├── business/                    # 💼 Lógica de negocio
│   │   ├── __init__.py              # Exporta servicios
│   │   ├── auth_service.py          # Autenticación y usuarios
│   │   └── session_service.py       # Sesiones y compras de juegos
│   │
│   └── api/                         # 🌐 API REST
│       ├── __init__.py              # create_app()
│       ├── app.py                   # Factory de Flask
│       └── routes/                  # Blueprints
│           ├── auth.py              # POST /auth/login, /auth/register
│           ├── games.py             # CRUD /games
│           └── sessions.py          # /sessions endpoints
│
├── data/                            # 📂 Datos persistidos (auto-generado)
│   ├── games.db                     # SQLite
│   ├── games.json                   # JSON
│   └── games.xml                    # XML
│
├── demo_simple.py                   # 🚀 Demo rápida CRUD básico
├── ejemplo_uso.py                   # 📚 Demo completa con servicios
├── requirements.txt                 # 📦 Dependencias
└── README.md                        # 📖 Este archivo
```

<br>

---

## 🚀 Instalación

### Requisitos
- Python 3.10 o superior
- pip (gestor de paquetes)

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/AgusMADEV/JVDATAACCESS.git
cd JVDATAACCESS

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

<br>

---

## 💻 Ejemplos de uso

### 🚀 Inicio Rápido

```python
from data_access_framework import create_framework
from data_access_framework.models import Game, Studio

# Crear framework con SQLite (o 'json', 'xml', 'csv', 'txt')
framework = create_framework(data_format='sqlite')

# Obtener repositorios
game_repo = framework.get_repository('Game')
studio_repo = framework.get_repository('Studio')

# Crear estudio
estudio = Studio(
    name='FromSoftware',
    founded_year=1986,
    country='Japón',
    website='https://www.fromsoftware.jp'
)
studio_repo.save(estudio)

# Crear juego
juego = Game(
    title='Elden Ring',
    studio_id=estudio.id,
    platform='Multi-platform',
    genre='Action RPG',
    release_year=2022,
    rating=9.5,
    price=59.99,
    playtime_hours=80,
    multiplayer=True
)
game_repo.save(juego)

# Listar todos los juegos
juegos = game_repo.load_all()
print(f"Total de juegos: {len(juegos)}")
```

### 🔐 Autenticación

```python
# Obtener servicio de autenticación
auth_service = framework.get_service('auth')

# Registrar nuevo jugador
player = auth_service.register_player(
    username='gamer123',
    email='gamer@example.com',
    password='mi_password_segura'
)

# Autenticar jugador
authenticated = auth_service.authenticate(
    email='gamer@example.com',
    password='mi_password_segura'
)

if authenticated:
    print(f"¡Bienvenido {authenticated.username}!")
else:
    print("Credenciales inválidas")
```

### 🎮 Gestión de Sesiones de Juego

```python
# Obtener servicio de sesiones
session_service = framework.get_service('session')

# Crear sesión (comprar juego)
session = session_service.create_session(
    game_id=juego.id,
    player_id=player.id
)

# Registrar horas jugadas
session_service.add_playtime(
    session_id=session.id,
    hours=5.5
)

# Marcar como completado
session_service.mark_completed(
    session_id=session.id,
    completed=True
)

# Obtener estadísticas del jugador
stats = session_service.get_player_stats(player.id)
print(f"Juegos comprados: {stats['total_games']}")
print(f"Horas totales: {stats['total_hours']}")
```

### 🔄 Cambiar Formato de Persistencia

```python
# Es tan simple como cambiar un parámetro
framework_json = create_framework(data_format='json')
framework_xml = create_framework(data_format='xml')
framework_csv = create_framework(data_format='csv')

# El código de tu aplicación no cambia,
# solo cambia dónde se guardan los datos
```

### 📊 Búsquedas y Filtros

```python
# Buscar juegos por género
rpg_games = game_repo.find_by(genre='RPG')

# Buscar juegos de un estudio
games_by_studio = game_repo.find_by(studio_id=estudio.id)

# Buscar por múltiples criterios
multiplayer_rpgs = [
    game for game in game_repo.load_all()
    if game.genre == 'RPG' and game.multiplayer
]

# Juegos recientes con buen rating
good_recent_games = [
    game for game in game_repo.load_all()
    if game.release_year >= 2020 and game.rating >= 8.0
]
```

### 🎯 Ejecutar las Demos

```bash
# Demo simple (CRUD básico con SQLite)
python demo_simple.py

# Demo completa (autenticación, sesiones, estadísticas)
python ejemplo_uso.py
```

<br>

---

## 🌐 API REST

### 🔧 Iniciar el Servidor

```python
# Crear framework con API habilitada
framework = create_framework(
    data_format='sqlite',
    config={
        'api.enabled': True,
        'api.port': 5000,
        'api.debug': True
    }
)

# Iniciar servidor
framework.start_api()
# Servidor en http://localhost:5000
```

### 📍 Endpoints Disponibles

#### Autenticación

| Método | Endpoint | Autenticación | Descripción |
|--------|----------|---------------|-------------|
| `POST` | `/auth/register` | ❌ | Registrar nuevo jugador |
| `POST` | `/auth/login` | ❌ | Obtener token JWT |

#### Juegos

| Método | Endpoint | Autenticación | Descripción |
|--------|----------|---------------|-------------|
| `GET` | `/games` | ✅ | Listar todos los juegos |
| `GET` | `/games/<id>` | ✅ | Obtener juego por ID |
| `POST` | `/games` | ✅ Admin | Crear nuevo juego |
| `PUT` | `/games/<id>` | ✅ Admin | Actualizar juego |
| `DELETE` | `/games/<id>` | ✅ Admin | Eliminar juego |

#### Sesiones de Juego

| Método | Endpoint | Autenticación | Descripción |
|--------|----------|---------------|-------------|
| `POST` | `/sessions` | ✅ | Crear sesión (comprar) |
| `GET` | `/sessions/player/<id>` | ✅ | Sesiones del jugador |
| `PUT` | `/sessions/<id>/playtime` | ✅ | Actualizar horas jugadas |
| `PUT` | `/sessions/<id>/complete` | ✅ | Marcar como completado |

### 🔨 Ejemplos con cURL

```bash
# Registrar jugador
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "gamer123",
    "email": "gamer@example.com",
    "password": "password123"
  }'

# Login (obtener token)
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "gamer@example.com",
    "password": "password123"
  }'

# Listar juegos (con autenticación)
curl -X GET http://localhost:5000/games \
  -H "Authorization: Bearer TU_TOKEN_JWT"

# Crear nuevo juego (requiere rol admin)
curl -X POST http://localhost:5000/games \
  -H "Authorization: Bearer TU_TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Dark Souls III",
    "studio_id": "uuid-del-estudio",
    "platform": "Multi-platform",
    "genre": "Action RPG",
    "release_year": 2016,
    "rating": 9.0,
    "price": 39.99,
    "playtime_hours": 60
  }'
```

<br>

---

## 🔐 Seguridad

### Contraseñas
- Hash **HMAC-SHA256** con sal aleatoria única por usuario
- Sal de 16 bytes generada con `secrets.token_hex(16)`
- Formato: `{salt}${hash}` para almacenamiento seguro

### Autenticación JWT
- Tokens firmados con HS256
- Expiración configurable (24h por defecto)
- Incluye role del usuario en el payload

### Roles de Usuario
- **player**: Puede ver juegos y crear sesiones propias
- **moderator**: Puede editar información de juegos
- **admin**: Acceso completo (crear, editar, eliminar)

### Validaciones
- Email con expresión regular RFC-compliant
- Contraseñas de longitud mínima
- Validación de rangos (años, ratings, precios)
- Sanitización de entradas

<br>

---

## 🛠 Stack Tecnológico

| Componente | Tecnología | Propósito |
|------------|-----------|-----------|
| **Lenguaje** | Python 3.10+ | Desarrollo principal |
| **Web Framework** | Flask 2.3+ | API REST |
| **Auth** | Flask-JWT-Extended | Tokens JWT |
| **ORM** | SQLAlchemy 2.0+ | Acceso a SQLite |
| **XML** | lxml 4.9+ | Parsing/generación XML |
| **Parsing** | dateutil 2.8+ | Manejo de fechas |
| **Validación** | jsonschema 4.19+ | Validación de datos |
| **CORS** | Flask-CORS 4.0+ | Cross-Origin requests |

<br>

---

## 📚 Casos de Uso

### Tienda de Videojuegos
- Catálogo de juegos con búsqueda y filtros
- Sistema de compras (sesiones)
- Perfiles de usuario con historial
- Recomendaciones basadas en género

### Biblioteca de Juegos Personal
- Tracking de juegos comprados
- Registro de horas jugadas
- Lista de juegos completados
- Estadísticas personales

### Sistema de Gestión de Estudio
- Catálogo de juegos desarrollados
- Información de estudios colaboradores
- Análisis de ratings y ventas
- Gestión de lanzamientos

### Plataforma Social Gaming
- Perfiles de jugadores con niveles
- Sistema de logros
- Estadísticas comparativas
- Rankings y leaderboards

<br>

---

## 🎓 Patrones de Diseño Implementados

### Factory Pattern
```python
# DataAccessFramework crea el gestor correcto automáticamente
framework = create_framework(data_format='json')
# Internamente instancia JsonManager sin que lo sepas
```

### Repository Pattern
```python
# Interfaz unificada para todas las entidades
game_repo = framework.get_repository('Game')
game_repo.save(juego)    # Funciona igual con cualquier backend
game_repo.load(id)       # SQLite, JSON, XML... transparente
game_repo.find_by(...)   # Misma API para todo
```

### Strategy Pattern
```python
# Cada DataManager implementa la misma interfaz
# pero con estrategia de almacenamiento diferente
class DataManager:
    def save(self, entity): pass
    def load(self, entity_id): pass
    def delete(self, entity_id): pass

# Implementaciones: DbManager, JsonManager, XmlManager...
```

### Dependency Injection
```python
# Los servicios reciben sus dependencias
class GameSessionService:
    def __init__(self, entity_manager, config):
        self.entity_manager = entity_manager
        # No crea sus propias dependencias
```

<br>

---

## 📜 Licencia

Este proyecto está bajo la licencia **MIT**. Eres libre de usarlo, modificarlo y distribuirlo.

---

<div align="center">

### 🎮 JVDATAACCESS
*Framework de Gestión de Videojuegos con Persistencia Multi-Formato*

<br>

Desarrollado con ❤️ por [Agustín Morcillo](https://github.com/AgusMADEV)

[![GitHub](https://img.shields.io/badge/GitHub-AgusMADEV-181717?style=flat-square&logo=github)](https://github.com/AgusMADEV)

<br>

**DAM 2526** • 2026

</div>
