"""
JVExceptions - Excepciones personalizadas para JVDataAccess
Versión: 2.0.0

Define excepciones específicas para manejo robusto de errores
"""


class JVDBException(Exception):
    """Excepción base para todas las excepciones de JVDB"""
    pass


class ConnectionError(JVDBException):
    """Error al establecer conexión con la base de datos"""
    pass


class QueryError(JVDBException):
    """Error al ejecutar una consulta SQL"""
    pass


class TransactionError(JVDBException):
    """Error durante una transacción"""
    pass


class PoolExhaustedError(JVDBException):
    """El pool de conexiones está agotado"""
    pass


class ConfigurationError(JVDBException):
    """Error en la configuración"""
    pass


class ValidationError(JVDBException):
    """Error de validación de datos"""
    pass
