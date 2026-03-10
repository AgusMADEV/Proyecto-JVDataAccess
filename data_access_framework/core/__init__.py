"""
Core - Núcleo del framework de acceso a datos.

Incluye el framework principal, gestor de entidades,
configuración y migraciones.
"""

from .data_access_framework import DataAccessFramework, FrameworkConfig
from .entity_manager import EntityManager, Repository
from .config_manager import ConfigManager
from .migration_manager import MigrationManager

__all__ = [
    'DataAccessFramework',
    'FrameworkConfig',
    'EntityManager',
    'Repository',
    'ConfigManager',
    'MigrationManager',
]
