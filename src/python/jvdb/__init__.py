"""
JVDB - Clase de Abstracción para Acceso a Base de Datos
Versión: 2.0.0

Soporta versión 1.0 (legacy) y versión 2.0 (actual) con:
- Pool de conexiones
- Sistema de logging
- Transacciones
- CRUD optimizado
- Manejo robusto de errores
"""

# Versión 1.0 (legacy)
from .jvdb import JVDB

# Versión 2.0 (actual)
from .jvdb2 import JVDB2
from .connection_pool import JVConnectionPool, PooledConnection
from .logger import JVLogger
from .exceptions import (
    JVDBException,
    ConnectionError,
    QueryError,
    TransactionError,
    PoolExhaustedError,
    ConfigurationError,
    ValidationError
)

__version__ = "2.0.0"

__all__ = [
    # v1.0
    'JVDB',
    # v2.0
    'JVDB2',
    'JVConnectionPool',
    'PooledConnection',
    'JVLogger',
    # Exceptions
    'JVDBException',
    'ConnectionError',
    'QueryError',
    'TransactionError',
    'PoolExhaustedError',
    'ConfigurationError',
    'ValidationError'
]

