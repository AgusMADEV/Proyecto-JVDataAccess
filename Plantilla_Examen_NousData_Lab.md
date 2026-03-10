# NousData-Lab — Plantilla de Examen

**Alumno:** Luis Rodríguez Cedeño · **DNI:** 53945291X  
**Módulo:** Acceso a Datos · **Curso:** DAM2 2025/26

---

## 1. Introducción

- **Qué es:** Framework Python de acceso a datos multi-formato (JSON, CSV, XML, TXT, SQLite)
- **Contexto:** Módulo de Acceso a Datos — patrones Repository, Factory, capas de negocio, API REST
- **Objetivos principales:**
  - Framework reutilizable con 5 formatos de persistencia intercambiables
  - Patrón Repository genérico con `EntityManager`
  - Servicios de negocio (auth HMAC-SHA256, préstamos, reportes)
  - API REST con Flask + JWT + 4 blueprints
  - Migración automática entre formatos
- **Tecnologías clave:**
  - Python 3.11, dataclasses, ABC (clases abstractas), typing (generics)
  - Flask + Flask-CORS, PyJWT (JSON Web Tokens)
  - hashlib + secrets (HMAC-SHA256 salteado), sqlite3, json, csv, xml.etree
- **Arquitectura:** `core/` (DataAccessFramework, EntityManager, ConfigManager, MigrationManager) → `models/` (BaseEntity, Book, Author, User, Loan, Category) → `data_managers/` (ABC + Factory + 5 implementaciones) → `business/` (AuthService, LoanService, ReportService) → `api/` (Flask app factory + 4 blueprints)

---

## 2. Desarrollo de las partes

### 2.1 Modelos con dataclasses y validación

- `BaseEntity`: uuid auto-generado, `created_at`, `updated_at`, `to_dict()`, `from_dict()`
- Herencia: `Book(BaseEntity)`, `Author(BaseEntity)`, `User(BaseEntity)`, `Loan(BaseEntity)`, `Category(BaseEntity)`
- Validación en `__post_init__` + `_validate()`

```python
@dataclass
class BaseEntity:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for field_name in self.__dataclass_fields__:
            value = getattr(self, field_name)
            result[field_name] = value.isoformat() if isinstance(value, datetime) else value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseEntity':
        valid_fields = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)

@dataclass
class Book(BaseEntity):
    title: str = ""
    author_id: str = ""
    isbn: str = ""
    genre: str = ""
    year: int = datetime.now().year
    pages: int = 0
    available: bool = True

    def _validate(self):
        if not self.title.strip():
            raise ValueError("El título es obligatorio")
```

> **Explicación:** `BaseEntity` genera un UUID automáticamente y serializa/deserializa con `to_dict()`/`from_dict()`. Los modelos hijos heredan y validan campos en `__post_init__`.

### 2.2 ABC DataManager + Factory Pattern

- `DataManager(ABC)`: interfaz abstracta con `save()`, `load()`, `load_all()`, `delete()`, `search()`
- `DataManagerFactory`: registro estático de gestores + método `create_manager(format, entity_class)`
- 5 implementaciones concretas: JSON, CSV, XML, TXT, SQLite (DB)

```python
class DataManager(ABC):
    def __init__(self, base_path: str = "data"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

    @abstractmethod
    def save(self, entity) -> bool: pass
    @abstractmethod
    def load(self, entity_id: str): pass
    @abstractmethod
    def load_all(self) -> List: pass
    @abstractmethod
    def delete(self, entity_id: str) -> bool: pass
    @abstractmethod
    def search(self, criteria: Dict[str, Any]) -> List: pass

class DataManagerFactory:
    _managers = {}

    @classmethod
    def register_manager(cls, format_type: str, manager_class):
        cls._managers[format_type.lower()] = manager_class

    @classmethod
    def create_manager(cls, format_type: str, entity_class, base_path="data"):
        return cls._managers[format_type.lower()](entity_class, base_path)

# Registro de gestores
DataManagerFactory.register_manager('json', JSONDataManager)
DataManagerFactory.register_manager('xml', XMLDataManager)
DataManagerFactory.register_manager('csv', CSVDataManager)
DataManagerFactory.register_manager('txt', TXTDataManager)
DataManagerFactory.register_manager('sqlite', DBDataManager)
```

> **Explicación:** ABC obliga a implementar todos los métodos abstractos. La Factory desacopla la creación: basta cambiar el string del formato para usar otro gestor sin tocar código cliente.

### 2.3 JSONDataManager — Implementación concreta

- Hereda de `DataManager`, almacena en archivos `.json` con `json.dump/load`
- CRUD completo: `save()` (insert or update), `load_all()`, `delete()`, `search()` por criterios

```python
class JSONDataManager(DataManager):
    def __init__(self, entity_class, base_path="data"):
        super().__init__(base_path)
        self.entity_class = entity_class
        self.file_path = self.base_path / f"{entity_class.__name__.lower()}s.json"

    def save(self, entity) -> bool:
        entities = self.load_all()
        found = False
        for i, e in enumerate(entities):
            if e.id == entity.id:
                entities[i] = entity
                found = True
                break
        if not found:
            entities.append(entity)
        return self._write_all(entities)

    def _write_all(self, entities) -> bool:
        data = {f"{self.entity_name}s": [e.to_dict() for e in entities]}
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
```

> **Explicación:** Carga todas las entidades del JSON, busca si ya existe (por id) para actualizar, si no la añade. Serializa con `to_dict()` y guarda todo el array.

### 2.4 AuthService — Autenticación HMAC-SHA256

- Hash salteado: salt aleatorio (16 bytes hex) + SHA-256
- Login: `authenticate(email, password)` → verifica hash
- Registro: `register_user()` → valida email único, rol válido
- RBAC: `authorize(user, action)` → permisos por rol (user/librarian/admin)

```python
class AuthService:
    def __init__(self, entity_manager):
        self.user_repo = entity_manager.get_repository(User)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        users = self.user_repo.find_by(email=email)
        if not users:
            return None
        user = users[0]
        if not user.active or not self._verify_password(password, user.password_hash):
            return None
        return user

    def _hash_password(self, password: str) -> str:
        salt = secrets.token_hex(16)
        hashed = hashlib.sha256((salt + password).encode()).hexdigest()
        return f"{salt}${hashed}"

    def _verify_password(self, password: str, stored: str) -> bool:
        salt, hashed = stored.split('$', 1)
        return hashlib.sha256((salt + password).encode()).hexdigest() == hashed
```

> **Explicación:** Se genera un salt aleatorio de 16 bytes. Se concatena salt+password y se hashea con SHA-256. Para verificar, se extrae el salt del hash almacenado y se compara.

### 2.5 API REST Flask con JWT y Blueprints

- `create_app(framework)` → app factory pattern
- Decorador `@token_required` para proteger endpoints
- 4 blueprints: `auth` (login/register), `books` (CRUD), `loans` (gestión préstamos), `reports` (estadísticas)

```python
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token requerido"}), 401
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            request.current_user = user_repo.load(payload['user_id'])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        return f(*args, **kwargs)
    return decorated

def generate_token(user_id: str, app: Flask) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
```

> **Explicación:** El decorador extrae el token JWT del header Authorization, lo decodifica con la clave secreta y verifica expiración. Si es válido, inyecta el usuario en `request.current_user`.

### 2.6 DataAccessFramework — Clase coordinadora

- Inicializa todos los componentes: Factory, EntityManager, servicios de negocio
- API pública: `get_repository()`, `get_service()`, `start_api()`, `migrate_data()`
- Puede arrancar API en hilo separado (`blocking=False`)

```python
class DataAccessFramework:
    def __init__(self, config_path=None, **config_overrides):
        self.config = self._load_config(config_path, config_overrides)
        self.data_factory = DataManagerFactory()
        self.entity_manager = EntityManager(self.data_factory, self.config.database_format)
        self.loan_service = LoanService(self.entity_manager)
        self.report_service = ReportService(self.entity_manager)
        self.auth_service = AuthService(self.entity_manager)

    def start_api(self, host=None, port=None, blocking=True):
        app = create_app(self)
        if blocking:
            app.run(host=host, port=port)
        else:
            threading.Thread(target=lambda: app.run(host=host, port=port), daemon=True).start()

    def migrate_data(self, from_format: str, to_format: str):
        migrator = MigrationManager(self.entity_manager)
        migrator.migrate(from_format, to_format)
```

> **Explicación:** Orquesta todo: crea los managers según el formato configurado, instancia servicios y puede arrancar la API Flask. La migración lee en un formato y escribe en otro.

---

## 3. Presentación del proyecto

- **Flujo:** Crear framework → Elegir formato → CRUD entidades via repositorios → Servicios de negocio → API REST
- **Punto fuerte:** Intercambio de formato transparente (JSON↔CSV↔XML↔TXT↔SQLite)
- **Demo:** `python ejemplo_uso.py` o `python demo_simple.py` → CRUD completo + migración
- **Arquitectura limpia:** Cada capa aislada, Domain-driven, testeable

---

## 4. Conclusión

- **Competencias:** Patrón Repository genérico, Factory, ABC, dataclasses, JWT, Flask blueprints
- **Patrones clave:** Factory (gestores), Repository (EntityManager), Strategy (formatos intercambiables)
- **Seguridad:** HMAC-SHA256 con salt, JWT con expiración, RBAC por roles
- **Extensibilidad:** Añadir nuevo formato = implementar DataManager + registrar en Factory
- **Valoración:** Framework profesional que demuestra acceso a datos multi-formato con capas de negocio y API REST
