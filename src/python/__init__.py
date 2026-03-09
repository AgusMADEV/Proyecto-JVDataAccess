"""
JVDataAccess - Sistema Modular de Acceso a Datos
Versión: 1.0.0

Componentes:
- YourSQL: Conector MySQL personalizado
- JVDB: Abstracción de base de datos
"""

# Imports flexibles para compatibilidad
try:
    from .yoursql import YourSQLConnection, YourSQLQueryBuilder
    from .jvdb import JVDB
except ImportError:
    # Si falla el import relativo, intentar absoluto
    import sys
    import os
    # No hacer nada, los módulos se importarán directamente

__version__ = "1.0.0"
__all__ = ['YourSQLConnection', 'YourSQLQueryBuilder', 'JVDB']
