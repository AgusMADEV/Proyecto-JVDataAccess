"""
NousData-Lab - Framework genérico de acceso a datos multi-formato

Proporciona una abstracción completa para el acceso a datos en múltiples
formatos (SQLite, JSON, XML, CSV, TXT) con API REST, servicios de negocio
reutilizables y arquitectura extensible.

Autor: Luis Rodrigo Cepeda Villaverde - DAM2
Versión: 2.1.0
"""

__version__ = "2.1.0"
__author__ = "Luis Rodrigo Cepeda Villaverde"
__description__ = "Framework genérico de acceso a datos con múltiples formatos"

from .core.entity_manager import EntityManager
from .core.data_access_framework import DataAccessFramework
from .models import Game, Studio, Player, GameSession, Genre
from .business import GameSessionService, AuthService

# API pública principal
__all__ = [
    'DataAccessFramework',
    'EntityManager',
    'Game', 'Studio', 'Player', 'GameSession', 'Genre',
    'GameSessionService', 'AuthService'
]

# Función de conveniencia para crear framework rápidamente
def create_framework(config_path: str = None, **config):
    """
    Crea una instancia del framework con configuración opcional.

    Args:
        config_path: Ruta al archivo de configuración JSON
        **config: Configuración directa como parámetros

    Returns:
        DataAccessFramework: Instancia configurada del framework
    """
    return DataAccessFramework(config_path=config_path, **config)