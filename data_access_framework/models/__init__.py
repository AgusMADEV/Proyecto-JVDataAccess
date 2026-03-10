"""
Modelos de datos del framework

Incluye todas las entidades del sistema con validación completa.

Autor: DAM2526
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import uuid


@dataclass
class BaseEntity:
    """Entidad base con campos comunes."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(self.updated_at)

    def to_dict(self) -> Dict[str, Any]:
        """Convertir entidad a diccionario."""
        result = {}
        for field_name, field_info in self.__dataclass_fields__.items():
            value = getattr(self, field_name)
            if isinstance(value, datetime):
                result[field_name] = value.isoformat()
            else:
                result[field_name] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseEntity':
        """Crear entidad desde diccionario, filtrando campos desconocidos."""
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data and isinstance(data['updated_at'], str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        # Filtrar campos que no pertenecen al dataclass para evitar TypeError
        valid_fields = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)


@dataclass
class Game(BaseEntity):
    """Modelo de Videojuego."""
    title: str = ""
    studio_id: str = ""
    platform: str = ""  # PC, PlayStation, Xbox, Nintendo Switch, Mobile
    genre: str = ""
    release_year: int = datetime.now().year
    rating: float = 0.0  # Calificación 0-10
    price: float = 0.0
    playtime_hours: int = 0  # Horas estimadas para completar
    multiplayer: bool = False
    genre_id: Optional[str] = None
    available: bool = True

    def __post_init__(self):
        super().__post_init__()
        self._validate()

    def _validate(self):
        """Validar campos del videojuego."""
        if not self.title.strip():
            raise ValueError("El título es obligatorio")

        valid_platforms = ["PC", "PlayStation", "Xbox", "Nintendo Switch", "Mobile", "Multi-platform"]
        if self.platform and self.platform not in valid_platforms:
            raise ValueError(f"Plataforma inválida. Debe ser: {', '.join(valid_platforms)}")

        if self.release_year < 1970 or self.release_year > datetime.now().year + 2:
            raise ValueError("Año de lanzamiento inválido")

        if self.rating < 0 or self.rating > 10:
            raise ValueError("Calificación debe estar entre 0 y 10")

        if self.price < 0:
            raise ValueError("El precio no puede ser negativo")

        if self.playtime_hours < 0:
            raise ValueError("Las horas de juego no pueden ser negativas")


@dataclass
class Studio(BaseEntity):
    """Modelo de Estudio de Desarrollo."""
    name: str = ""
    founded_year: Optional[int] = None
    country: str = ""
    website: str = ""
    description: str = ""

    def __post_init__(self):
        super().__post_init__()
        self._validate()

    def _validate(self):
        """Validar campos del estudio."""
        if not self.name.strip():
            raise ValueError("El nombre del estudio es obligatorio")

        if self.founded_year and (self.founded_year < 1950 or self.founded_year > datetime.now().year):
            raise ValueError("Año de fundación inválido")

    @property
    def display_name(self) -> str:
        """Nombre del estudio para mostrar."""
        if self.founded_year:
            return f"{self.name} ({self.founded_year})"
        return self.name


@dataclass
class Player(BaseEntity):
    """Modelo de Jugador."""
    username: str = ""
    email: str = ""
    password_hash: str = ""
    role: str = "player"  # player, admin, moderator
    active: bool = True
    level: int = 1
    total_playtime_hours: float = 0.0

    def __post_init__(self):
        super().__post_init__()
        self._validate()

    def _validate(self):
        """Validar campos del jugador."""
        if not self.username.strip():
            raise ValueError("El nombre de usuario es obligatorio")

        if not self._validate_email(self.email):
            raise ValueError("Email inválido")

        if self.role not in ["player", "admin", "moderator"]:
            raise ValueError("Rol de jugador inválido")
        
        if self.level < 1:
            raise ValueError("El nivel debe ser al menos 1")

    def _validate_email(self, email: str) -> bool:
        """Validar formato de email."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @property
    def display_name(self) -> str:
        """Nombre para mostrar del jugador."""
        return f"{self.username} (Lv.{self.level})"

    def set_password(self, password: str):
        """Establecer contraseña hasheada con sal (HMAC-SHA256)."""
        import hashlib, secrets
        salt = secrets.token_hex(16)
        hashed = hashlib.sha256((salt + password).encode()).hexdigest()
        self.password_hash = f"{salt}${hashed}"

    def check_password(self, password: str) -> bool:
        """Verificar contraseña contra hash con sal."""
        import hashlib
        if '$' not in self.password_hash:
            # Compatibilidad con hashes legacy sin sal
            return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
        salt, stored_hash = self.password_hash.split('$', 1)
        return stored_hash == hashlib.sha256((salt + password).encode()).hexdigest()
    
    def add_playtime(self, hours: float):
        """Añadir horas de juego y actualizar nivel."""
        self.total_playtime_hours += hours
        # Subir nivel cada 10 horas de juego
        self.level = int(self.total_playtime_hours // 10) + 1


@dataclass
class Genre(BaseEntity):
    """Modelo de Género de Videojuego."""
    name: str = ""
    description: str = ""
    parent_id: Optional[str] = None  # Para géneros jerárquicos (ej: RPG -> JRPG)

    def __post_init__(self):
        super().__post_init__()
        self._validate()

    def _validate(self):
        """Validar campos del género."""
        if not self.name.strip():
            raise ValueError("El nombre del género es obligatorio")


@dataclass
class GameSession(BaseEntity):
    """Modelo de Sesión de Juego/Compra."""
    game_id: str = ""
    player_id: str = ""
    purchase_date: datetime = field(default_factory=datetime.now)
    playtime_hours: float = 0.0
    completed: bool = False
    achievements_unlocked: int = 0
    last_played: Optional[datetime] = None
    status: str = "active"  # active, completed, abandoned
    rating: Optional[float] = None  # Calificación personal del jugador (0-10)
    notes: str = ""

    def __post_init__(self):
        super().__post_init__()
        if isinstance(self.purchase_date, str):
            self.purchase_date = datetime.fromisoformat(self.purchase_date)
        if isinstance(self.last_played, str):
            self.last_played = datetime.fromisoformat(self.last_played)
        self._validate()

    def _validate(self):
        """Validar campos de la sesión de juego."""
        if not self.game_id:
            raise ValueError("El ID del juego es obligatorio")

        if not self.player_id:
            raise ValueError("El ID del jugador es obligatorio")

        if self.playtime_hours < 0:
            raise ValueError("Las horas de juego no pueden ser negativas")

        if self.achievements_unlocked < 0:
            raise ValueError("Los logros desbloqueados no pueden ser negativos")

        if self.rating is not None and (self.rating < 0 or self.rating > 10):
            raise ValueError("La calificación debe estar entre 0 y 10")

        if self.status not in ["active", "completed", "abandoned"]:
            raise ValueError("Estado de sesión inválido")

    @property
    def days_since_last_played(self) -> int:
        """Días desde la última vez que se jugó."""
        if not self.last_played:
            return (datetime.now() - self.purchase_date).days
        return (datetime.now() - self.last_played).days

    def add_playtime(self, hours: float):
        """Añadir horas de juego."""
        self.playtime_hours += hours
        self.last_played = datetime.now()
        self.updated_at = datetime.now()

    def mark_completed(self):
        """Marcar juego como completado."""
        self.completed = True
        self.status = "completed"
        self.updated_at = datetime.now()

    def mark_abandoned(self):
        """Marcar juego como abandonado."""
        self.status = "abandoned"
        self.updated_at = datetime.now()


# Exportar todas las clases
# Exportar todas las clases
__all__ = ["Game", "Studio", "Player", "GameSession", "Genre", "BaseEntity"]