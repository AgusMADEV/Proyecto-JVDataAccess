<?php
/**
 * JVExceptions - Excepciones personalizadas para JVDataAccess (PHP)
 * Versión: 2.0.0
 * 
 * Define excepciones específicas para manejo robusto de errores
 */

namespace JVDB\Exceptions;

use Exception;

/**
 * Excepción base para todas las excepciones de JVDB
 */
class JVDBException extends Exception {}

/**
 * Error al establecer conexión con la base de datos
 */
class ConnectionException extends JVDBException {}

/**
 * Error al ejecutar una consulta SQL
 */
class QueryException extends JVDBException {}

/**
 * Error durante una transacción
 */
class TransactionException extends JVDBException {}

/**
 * El pool de conexiones está agotado
 */
class PoolExhaustedException extends JVDBException {}

/**
 * Error en la configuración
 */
class ConfigurationException extends JVDBException {}

/**
 * Error de validación de datos
 */
class ValidationException extends JVDBException {}
