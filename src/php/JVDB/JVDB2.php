<?php
/**
 * JVDB 2.0 - Clase de Abstracción para Acceso a Base de Datos (PHP)
 * Versión: 2.0.0
 * 
 * Versión mejorada con:
 * - Sistema de logging integrado
 * - Pool de conexiones
 * - Soporte para transacciones
 * - CRUD completo optimizado
 * - Manejo robusto de errores
 */

namespace JVDB;

require_once __DIR__ . '/../YourSQL/YourSQL.php';
require_once __DIR__ . '/JVConnectionPool.php';
require_once __DIR__ . '/JVLogger.php';
require_once __DIR__ . '/JVExceptions.php';

use YourSQL\YourSQLConnection;
use JVDB\Exceptions\ValidationException;
use JVDB\Exceptions\QueryException;
use JVDB\Exceptions\ConnectionException;
use JVDB\Exceptions\TransactionException;
use JVDB\Exceptions\PoolExhaustedException;
use JVDB\Exceptions\ConfigurationException;

class JVDB2 {
    private string $host;
    private string $usuario;
    private string $contrasena;
    private string $basedatos;
    private int $port;
    private JVLogger $logger;
    private bool $usePool;
    private ?JVConnectionPool $pool = null;
    private ?YourSQLConnection $conexion = null;
    private bool $inTransaction = false;
    
    /**
     * Constructor - Inicializa JVDB2 con los parámetros de conexión
     * 
     * @param string $host Dirección del servidor MySQL
     * @param string $usuario Usuario de la base de datos
     * @param string $contrasena Contraseña del usuario
     * @param string $basedatos Nombre de la base de datos
     * @param int $port Puerto de conexión
     * @param bool $usePool Usar pool de conexiones
     * @param array $poolConfig Configuración del pool
     * @param array $logConfig Configuración del logger
     */
    public function __construct(
        string $host,
        string $usuario,
        string $contrasena,
        string $basedatos,
        int $port = 3306,
        bool $usePool = true,
        array $poolConfig = [],
        array $logConfig = []
    ) {
        $this->host = $host;
        $this->usuario = $usuario;
        $this->contrasena = $contrasena;
        $this->basedatos = $basedatos;
        $this->port = $port;
        $this->usePool = $usePool;
        
        // Configurar logger
        $this->logger = JVLogger::getInstance('JVDB2', $logConfig);
        
        // Pool de conexiones o conexión simple
        if ($usePool) {
            $this->pool = new JVConnectionPool(
                $host,
                $usuario,
                $contrasena,
                $basedatos,
                $port,
                $poolConfig['min_size'] ?? 2,
                $poolConfig['max_size'] ?? 10,
                $poolConfig['max_lifetime'] ?? 3600,
                $poolConfig['timeout'] ?? 30,
                $this->logger
            );
            $this->logger->info("JVDB2 inicializado con pool de conexiones");
        } else {
            $this->conexion = new YourSQLConnection($host, $usuario, $contrasena, $basedatos, $port);
            if ($this->conexion->connect()) {
                $this->logger->connection($host, $basedatos, true);
            } else {
                $this->logger->connection($host, $basedatos, false);
                throw new ConnectionException("No se pudo conectar a $host/$basedatos");
            }
        }
    }
    
    /**
     * Obtiene una conexión del pool o la conexión directa
     * 
     * @return array [PooledConnection|YourSQLConnection, bool shouldRelease]
     */
    private function getConnection(): array {
        if ($this->usePool && !$this->inTransaction) {
            $pooledConn = $this->pool->acquire();
            return [$pooledConn->connection, true, $pooledConn];
        } else {
            return [$this->conexion, false, null];
        }
    }
    
    /**
     * Libera una conexión si es necesario
     */
    private function releaseConnection($pooledConn): void {
        if ($pooledConn && $this->usePool && !$this->inTransaction) {
            $this->pool->release($pooledConn);
        }
    }
    
    /**
     * Selecciona registros de una tabla con opciones avanzadas
     * 
     * @param string $tabla Nombre de la tabla
     * @param string|array $columnas Columnas a seleccionar
     * @param array|null $where Condiciones WHERE
     * @param string|null $orderBy Ordenamiento
     * @param int|null $limit Límite de resultados
     * @param int|null $offset Offset para paginación
     * @param string $formato 'json' o 'array'
     * @return string|array Datos en el formato especificado
     */
    public function seleccionar(
        string $tabla,
        $columnas = '*',
        ?array $where = null,
        ?string $orderBy = null,
        ?int $limit = null,
        ?int $offset = null,
        string $formato = 'array'
    ) {
        try {
            // Construir columnas
            $cols = is_array($columnas) ? implode(', ', $columnas) : $columnas;
            
            // Construir query
            $query = "SELECT $cols FROM $tabla";
            $params = [];
            
            // Agregar WHERE
            if ($where) {
                $conditions = [];
                foreach ($where as $col => $val) {
                    $conditions[] = "$col = ?";
                    $params[] = $val;
                }
                $query .= " WHERE " . implode(' AND ', $conditions);
            }
            
            // Agregar ORDER BY
            if ($orderBy) {
                $query .= " ORDER BY $orderBy";
            }
            
            // Agregar LIMIT y OFFSET
            if ($limit) {
                $query .= " LIMIT $limit";
                if ($offset) {
                    $query .= " OFFSET $offset";
                }
            }
            
            $this->logger->query($query, $params);
            
            list($conn, $shouldRelease, $pooledConn) = $this->getConnection();
            $resultado = $conn->executeQuery($query, $params);
            $this->releaseConnection($pooledConn);
            
            if ($resultado === null) {
                $resultado = [];
            }
            
            $this->logger->info(count($resultado) . " registros seleccionados de '$tabla'");
            
            if ($formato === 'json') {
                return json_encode($resultado, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
            }
            
            return $resultado;
            
        } catch (\Exception $e) {
            $this->logger->error("Error en seleccionar: {$e->getMessage()}");
            throw new QueryException("Error al seleccionar de $tabla: {$e->getMessage()}");
        }
    }
    
    /**
     * Selecciona un único registro
     * 
     * @param string $tabla Nombre de la tabla
     * @param int|null $identificador ID del registro
     * @param array|null $where Condiciones alternativas
     * @return array|null Registro o null
     */
    public function seleccionarUno(string $tabla, ?int $identificador = null, ?array $where = null): ?array {
        try {
            if ($identificador !== null) {
                $where = ['Identificador' => $identificador];
            } elseif ($where === null) {
                throw new ValidationException("Debe proporcionar identificador o where");
            }
            
            $resultados = $this->seleccionar($tabla, '*', $where, null, 1, null, 'array');
            return count($resultados) > 0 ? $resultados[0] : null;
            
        } catch (\Exception $e) {
            $this->logger->error("Error en seleccionarUno: {$e->getMessage()}");
            throw new QueryException("Error al seleccionar uno de $tabla: {$e->getMessage()}");
        }
    }
    
    /**
     * Inserta un nuevo registro
     * 
     * @param string $tabla Nombre de la tabla
     * @param array $datos Diccionario con columna => valor
     * @param bool $returnId Si true, devuelve array con info
     * @return int|array Filas afectadas o array con info
     */
    public function insertar(string $tabla, array $datos, bool $returnId = false) {
        try {
            if (empty($datos)) {
                throw new ValidationException("No se proporcionaron datos para insertar");
            }
            
            $columnas = implode(', ', array_keys($datos));
            $placeholders = implode(', ', array_fill(0, count($datos), '?'));
            $valores = array_values($datos);
            
            $query = "INSERT INTO $tabla ($columnas) VALUES ($placeholders)";
            $this->logger->query($query, $valores);
            
            list($conn, $shouldRelease, $pooledConn) = $this->getConnection();
            $resultado = $conn->executeQuery($query, $valores);
            
            // Obtener último ID insertado
            $lastId = method_exists($conn, 'getLastInsertId') ? 
                $conn->getLastInsertId() : 
                $conn->_connection->insert_id ?? null;
            
            $this->releaseConnection($pooledConn);
            
            $this->logger->info("Registro insertado en '$tabla'");
            
            if ($returnId) {
                return [
                    'rows_affected' => $resultado ?? 0,
                    'last_insert_id' => $lastId
                ];
            }
            
            return $resultado ?? 0;
            
        } catch (\Exception $e) {
            $this->logger->error("Error en insertar: {$e->getMessage()}");
            throw new QueryException("Error al insertar en $tabla: {$e->getMessage()}");
        }
    }
    
    /**
     * Inserta múltiples registros de forma optimizada
     * 
     * @param string $tabla Nombre de la tabla
     * @param array $registros Lista de arrays con los datos
     * @return int Total de filas insertadas
     */
    public function insertarMultiple(string $tabla, array $registros): int {
        try {
            if (empty($registros)) {
                return 0;
            }
            
            $total = 0;
            $this->beginTransaction();
            
            try {
                foreach ($registros as $registro) {
                    $total += $this->insertar($tabla, $registro);
                }
                $this->commit();
            } catch (\Exception $e) {
                $this->rollback();
                throw $e;
            }
            
            $this->logger->info("$total registros insertados en '$tabla'");
            return $total;
            
        } catch (\Exception $e) {
            $this->logger->error("Error en insertarMultiple: {$e->getMessage()}");
            throw new QueryException("Error al insertar múltiples en $tabla: {$e->getMessage()}");
        }
    }
    
    /**
     * Actualiza registros existentes
     * 
     * @param string $tabla Nombre de la tabla
     * @param array $datos Datos a actualizar
     * @param int|null $identificador ID del registro
     * @param array|null $where Condiciones alternativas
     * @return int Filas afectadas
     */
    public function actualizar(
        string $tabla,
        array $datos,
        ?int $identificador = null,
        ?array $where = null
    ): int {
        try {
            if (empty($datos)) {
                throw new ValidationException("No se proporcionaron datos para actualizar");
            }
            
            if ($identificador !== null) {
                $where = ['Identificador' => $identificador];
            } elseif ($where === null) {
                throw new ValidationException("Debe proporcionar identificador o where");
            }
            
            // Construir SET clause
            $setClause = implode(', ', array_map(fn($col) => "$col = ?", array_keys($datos)));
            $valores = array_values($datos);
            
            // Construir WHERE clause
            $whereConditions = [];
            foreach ($where as $col => $val) {
                $whereConditions[] = "$col = ?";
                $valores[] = $val;
            }
            
            $query = "UPDATE $tabla SET $setClause WHERE " . implode(' AND ', $whereConditions);
            $this->logger->query($query, $valores);
            
            list($conn, $shouldRelease, $pooledConn) = $this->getConnection();
            $resultado = $conn->executeQuery($query, $valores);
            $this->releaseConnection($pooledConn);
            
            $this->logger->info("$resultado registro(s) actualizado(s) en '$tabla'");
            return $resultado ?? 0;
            
        } catch (\Exception $e) {
            $this->logger->error("Error en actualizar: {$e->getMessage()}");
            throw new QueryException("Error al actualizar $tabla: {$e->getMessage()}");
        }
    }
    
    /**
     * Elimina registros de una tabla
     * 
     * @param string $tabla Nombre de la tabla
     * @param int|null $identificador ID del registro
     * @param array|null $where Condiciones alternativas
     * @return int Filas eliminadas
     */
    public function eliminar(string $tabla, ?int $identificador = null, ?array $where = null): int {
        try {
            if ($identificador !== null) {
                $where = ['Identificador' => $identificador];
            } elseif ($where === null) {
                throw new ValidationException("Debe proporcionar identificador o where");
            }
            
            // Construir WHERE clause
            $whereConditions = [];
            $valores = [];
            foreach ($where as $col => $val) {
                $whereConditions[] = "$col = ?";
                $valores[] = $val;
            }
            
            $query = "DELETE FROM $tabla WHERE " . implode(' AND ', $whereConditions);
            $this->logger->query($query, $valores);
            
            list($conn, $shouldRelease, $pooledConn) = $this->getConnection();
            $resultado = $conn->executeQuery($query, $valores);
            $this->releaseConnection($pooledConn);
            
            $this->logger->info("$resultado registro(s) eliminado(s) de '$tabla'");
            return $resultado ?? 0;
            
        } catch (\Exception $e) {
            $this->logger->error("Error en eliminar: {$e->getMessage()}");
            throw new QueryException("Error al eliminar de $tabla: {$e->getMessage()}");
        }
    }
    
    /**
     * Cuenta registros en una tabla
     * 
     * @param string $tabla Nombre de la tabla
     * @param array|null $where Condiciones opcionales
     * @return int Número de registros
     */
    public function contar(string $tabla, ?array $where = null): int {
        try {
            $query = "SELECT COUNT(*) as total FROM $tabla";
            $params = [];
            
            if ($where) {
                $conditions = [];
                foreach ($where as $col => $val) {
                    $conditions[] = "$col = ?";
                    $params[] = $val;
                }
                $query .= " WHERE " . implode(' AND ', $conditions);
            }
            
            list($conn, $shouldRelease, $pooledConn) = $this->getConnection();
            $resultado = $conn->executeQuery($query, $params);
            $this->releaseConnection($pooledConn);
            
            return $resultado[0]['total'] ?? 0;
            
        } catch (\Exception $e) {
            $this->logger->error("Error en contar: {$e->getMessage()}");
            throw new QueryException("Error al contar en $tabla: {$e->getMessage()}");
        }
    }
    
    /**
     * Verifica si existe al menos un registro
     * 
     * @param string $tabla Nombre de la tabla
     * @param array $where Condiciones de búsqueda
     * @return bool True si existe
     */
    public function existe(string $tabla, array $where): bool {
        return $this->contar($tabla, $where) > 0;
    }
    
    /**
     * Inicia una transacción
     */
    public function beginTransaction(): void {
        if ($this->inTransaction) {
            throw new TransactionException("Ya hay una transacción en curso");
        }
        
        $conn = $this->usePool ? $this->pool->acquire()->connection : $this->conexion;
        $conn->beginTransaction();
        $this->inTransaction = true;
        $this->conexion = $conn;
        $this->logger->transaction("BEGIN");
    }
    
    /**
     * Confirma una transacción
     */
    public function commit(): void {
        if (!$this->inTransaction) {
            throw new TransactionException("No hay transacción activa");
        }
        
        $this->conexion->commit();
        $this->inTransaction = false;
        $this->logger->transaction("COMMIT");
    }
    
    /**
     * Revierte una transacción
     */
    public function rollback(): void {
        if (!$this->inTransaction) {
            throw new TransactionException("No hay transacción activa");
        }
        
        $this->conexion->rollback();
        $this->inTransaction = false;
        $this->logger->transaction("ROLLBACK");
    }
    
    /**
     * Ejecuta una consulta SQL personalizada
     * 
     * @param string $query Consulta SQL
     * @param array|null $params Parámetros
     * @return mixed Resultados
     */
    public function consultaPersonalizada(string $query, ?array $params = null) {
        try {
            $this->logger->query($query, $params);
            
            list($conn, $shouldRelease, $pooledConn) = $this->getConnection();
            $resultado = $conn->executeQuery($query, $params);
            $this->releaseConnection($pooledConn);
            
            return $resultado;
            
        } catch (\Exception $e) {
            $this->logger->error("Error en consulta personalizada: {$e->getMessage()}");
            throw new QueryException("Error en consulta: {$e->getMessage()}");
        }
    }
    
    /**
     * Obtiene estadísticas del pool
     * 
     * @return array|null Estadísticas
     */
    public function getPoolStats(): ?array {
        return $this->pool ? $this->pool->getStats() : null;
    }
    
    /**
     * Cierra el pool o la conexión
     */
    public function cerrar(): void {
        try {
            if ($this->pool) {
                $this->pool->close();
                $this->logger->info("Pool de conexiones cerrado");
            } elseif ($this->conexion) {
                $this->conexion->disconnect();
                $this->logger->info("Conexión cerrada");
            }
        } catch (\Exception $e) {
            $this->logger->error("Error al cerrar: {$e->getMessage()}");
        }
    }
    
    /**
     * Destructor
     */
    public function __destruct() {
        try {
            $this->cerrar();
        } catch (\Exception $e) {
            // Ignorar errores en destructor
        }
    }
}
