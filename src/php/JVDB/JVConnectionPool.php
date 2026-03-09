<?php
/**
 * JVConnectionPool - Pool de Conexiones para YourSQL (PHP)
 * Versión: 2.0.0
 * 
 * Gestiona un pool de conexiones reutilizables para mejorar el rendimiento
 */

namespace JVDB;

require_once __DIR__ . '/../YourSQL/YourSQL.php';
require_once __DIR__ . '/JVLogger.php';
require_once __DIR__ . '/JVExceptions.php';

use YourSQL\YourSQLConnection;
use JVDB\Exceptions\PoolExhaustedException;
use JVDB\Exceptions\ConnectionException;

/**
 * Clase para gestionar una conexión del pool
 */
class PooledConnection {
    public YourSQLConnection $connection;
    public JVConnectionPool $pool;
    public bool $inUse = false;
    public float $createdAt;
    public float $lastUsed;
    
    public function __construct(YourSQLConnection $connection, JVConnectionPool $pool) {
        $this->connection = $connection;
        $this->pool = $pool;
        $this->createdAt = microtime(true);
        $this->lastUsed = microtime(true);
    }
}

/**
 * Pool de conexiones MySQL con gestión automática
 */
class JVConnectionPool {
    private array $config;
    private int $minSize;
    private int $maxSize;
    private int $maxLifetime;
    private int $timeout;
    private JVLogger $logger;
    private array $pool = [];
    private array $connections = [];
    private bool $closed = false;
    
    /**
     * Constructor del pool de conexiones
     * 
     * @param string $host Host del servidor MySQL
     * @param string $user Usuario de la base de datos
     * @param string $password Contraseña del usuario
     * @param string $database Nombre de la base de datos
     * @param int $port Puerto de conexión
     * @param int $minSize Número mínimo de conexiones
     * @param int $maxSize Número máximo de conexiones
     * @param int $maxLifetime Tiempo máximo de vida (segundos)
     * @param int $timeout Timeout para obtener conexión
     * @param JVLogger|null $logger Logger opcional
     */
    public function __construct(
        string $host,
        string $user,
        string $password,
        string $database,
        int $port = 3306,
        int $minSize = 2,
        int $maxSize = 10,
        int $maxLifetime = 3600,
        int $timeout = 30,
        ?JVLogger $logger = null
    ) {
        $this->config = [
            'host' => $host,
            'user' => $user,
            'password' => $password,
            'database' => $database,
            'port' => $port
        ];
        
        $this->minSize = $minSize;
        $this->maxSize = $maxSize;
        $this->maxLifetime = $maxLifetime;
        $this->timeout = $timeout;
        $this->logger = $logger ?? JVLogger::getInstance('JVPool');
        
        $this->initializePool();
    }
    
    /**
     * Inicializa el pool con conexiones mínimas
     */
    private function initializePool(): void {
        $this->logger->info("Inicializando pool con {$this->minSize} conexiones");
        
        for ($i = 0; $i < $this->minSize; $i++) {
            try {
                $conn = $this->createConnection();
                $this->pool[] = $conn;
            } catch (\Exception $e) {
                $this->logger->error("Error al crear conexión inicial: {$e->getMessage()}");
            }
        }
    }
    
    /**
     * Crea una nueva conexión
     * 
     * @return PooledConnection Nueva conexión del pool
     * @throws ConnectionException Si no se puede crear la conexión
     */
    private function createConnection(): PooledConnection {
        try {
            $connection = new YourSQLConnection(
                $this->config['host'],
                $this->config['user'],
                $this->config['password'],
                $this->config['database'],
                $this->config['port']
            );
            
            if (!$connection->connect()) {
                throw new ConnectionException("No se pudo establecer la conexión");
            }
            
            $pooledConn = new PooledConnection($connection, $this);
            $this->connections[] = $pooledConn;
            
            $this->logger->debug("Nueva conexión creada. Total: " . count($this->connections));
            return $pooledConn;
            
        } catch (\Exception $e) {
            $this->logger->error("Error al crear conexión: {$e->getMessage()}");
            throw new ConnectionException("Error al crear conexión: {$e->getMessage()}");
        }
    }
    
    /**
     * Obtiene una conexión del pool
     * 
     * @return PooledConnection Conexión lista para usar
     * @throws PoolExhaustedException Si no hay conexiones disponibles
     */
    public function acquire(): PooledConnection {
        if ($this->closed) {
            throw new ConnectionException("El pool está cerrado");
        }
        
        $startTime = microtime(true);
        
        while (true) {
            // Buscar conexión disponible
            foreach ($this->pool as $key => $pooledConn) {
                if (!$pooledConn->inUse && $this->isValid($pooledConn)) {
                    unset($this->pool[$key]);
                    $pooledConn->inUse = true;
                    $pooledConn->lastUsed = microtime(true);
                    $this->logger->debug("Conexión obtenida del pool");
                    return $pooledConn;
                }
            }
            
            // Si no hay disponibles y podemos crear más
            if (count($this->connections) < $this->maxSize) {
                $this->logger->info("Pool vacío, creando nueva conexión");
                $pooledConn = $this->createConnection();
                $pooledConn->inUse = true;
                return $pooledConn;
            }
            
            // Verificar timeout
            if (microtime(true) - $startTime > $this->timeout) {
                throw new PoolExhaustedException(
                    "No se pudo obtener conexión en {$this->timeout} segundos"
                );
            }
            
            // Esperar un poco antes de reintentar
            usleep(100000); // 100ms
        }
    }
    
    /**
     * Devuelve una conexión al pool
     * 
     * @param PooledConnection $pooledConn Conexión a devolver
     */
    public function release(PooledConnection $pooledConn): void {
        if ($this->closed) {
            return;
        }
        
        $pooledConn->inUse = false;
        $pooledConn->lastUsed = microtime(true);
        
        // Verificar si debe cerrarse por edad
        if (microtime(true) - $pooledConn->createdAt > $this->maxLifetime) {
            $this->logger->info("Conexión expirada, cerrando");
            $this->removeConnection($pooledConn);
            
            // Crear nueva si estamos bajo el mínimo
            if (count($this->connections) < $this->minSize) {
                $newConn = $this->createConnection();
                $this->pool[] = $newConn;
            }
        } else {
            $this->pool[] = $pooledConn;
            $this->logger->debug("Conexión devuelta al pool");
        }
    }
    
    /**
     * Verifica si una conexión es válida
     * 
     * @param PooledConnection $pooledConn Conexión a verificar
     * @return bool True si es válida
     */
    private function isValid(PooledConnection $pooledConn): bool {
        try {
            return $pooledConn->connection->isConnected();
        } catch (\Exception $e) {
            return false;
        }
    }
    
    /**
     * Elimina una conexión del pool
     * 
     * @param PooledConnection $pooledConn Conexión a eliminar
     */
    private function removeConnection(PooledConnection $pooledConn): void {
        try {
            $pooledConn->connection->disconnect();
        } catch (\Exception $e) {
            // Ignorar errores al cerrar
        }
        
        $key = array_search($pooledConn, $this->connections);
        if ($key !== false) {
            unset($this->connections[$key]);
            $this->connections = array_values($this->connections);
        }
        
        $this->logger->debug("Conexión eliminada. Total: " . count($this->connections));
    }
    
    /**
     * Cierra todas las conexiones del pool
     */
    public function close(): void {
        $this->logger->info("Cerrando pool de conexiones");
        $this->closed = true;
        
        $this->pool = [];
        
        foreach ($this->connections as $pooledConn) {
            try {
                $pooledConn->connection->disconnect();
            } catch (\Exception $e) {
                // Ignorar errores
            }
        }
        
        $this->connections = [];
        $this->logger->info("Pool cerrado");
    }
    
    /**
     * Obtiene estadísticas del pool
     * 
     * @return array Estadísticas del pool
     */
    public function getStats(): array {
        $total = count($this->connections);
        $inUse = 0;
        
        foreach ($this->connections as $conn) {
            if ($conn->inUse) {
                $inUse++;
            }
        }
        
        $available = $total - $inUse;
        
        return [
            'total_connections' => $total,
            'in_use' => $inUse,
            'available' => $available,
            'min_size' => $this->minSize,
            'max_size' => $this->maxSize,
            'is_closed' => $this->closed
        ];
    }
    
    /**
     * Destructor - cierra el pool
     */
    public function __destruct() {
        $this->close();
    }
}
