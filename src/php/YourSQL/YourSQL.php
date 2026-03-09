<?php
/**
 * YourSQL - Conector MySQL Personalizado para PHP
 * Versión: 1.0.0
 * 
 * Proporciona una capa de abstracción sobre MySQLi con funcionalidades mejoradas
 */

namespace YourSQL;

use mysqli;
use mysqli_result;
use Exception;

class YourSQLConnection {
    private mysqli $connection;
    private string $host;
    private string $user;
    private string $password;
    private string $database;
    private int $port;
    private string $charset;
    private bool $connected = false;
    
    /**
     * Constructor - Inicializa los parámetros de conexión
     * 
     * @param string $host Dirección del servidor MySQL
     * @param string $user Usuario de la base de datos
     * @param string $password Contraseña del usuario
     * @param string $database Nombre de la base de datos
     * @param int $port Puerto de conexión (por defecto 3306)
     * @param string $charset Codificación de caracteres (por defecto utf8mb4)
     */
    public function __construct(
        string $host,
        string $user,
        string $password,
        string $database,
        int $port = 3306,
        string $charset = 'utf8mb4'
    ) {
        $this->host = $host;
        $this->user = $user;
        $this->password = $password;
        $this->database = $database;
        $this->port = $port;
        $this->charset = $charset;
    }
    
    /**
     * Establece la conexión con la base de datos
     * 
     * @return bool True si la conexión fue exitosa
     * @throws Exception Si la conexión falla
     */
    public function connect(): bool {
        try {
            $this->connection = new mysqli(
                $this->host,
                $this->user,
                $this->password,
                $this->database,
                $this->port
            );
            
            if ($this->connection->connect_error) {
                throw new Exception("Error de conexión: " . $this->connection->connect_error);
            }
            
            // Configurar charset
            $this->connection->set_charset($this->charset);
            $this->connected = true;
            
            return true;
        } catch (Exception $e) {
            echo "❌ Error al conectar con MySQL: " . $e->getMessage() . "\n";
            $this->connected = false;
            return false;
        }
    }
    
    /**
     * Cierra la conexión con la base de datos
     */
    public function disconnect(): void {
        if ($this->connected && $this->connection) {
            $this->connection->close();
            $this->connected = false;
        }
    }
    
    /**
     * Verifica si la conexión está activa
     * 
     * @return bool True si hay conexión activa
     */
    public function isConnected(): bool {
        return $this->connected && $this->connection && $this->connection->ping();
    }
    
    /**
     * Obtiene la conexión MySQLi
     * 
     * @return mysqli Conexión MySQLi
     */
    public function getConnection(): mysqli {
        if (!$this->isConnected()) {
            $this->connect();
        }
        return $this->connection;
    }
    
    /**
     * Ejecuta una consulta SQL
     * 
     * @param string $query Consulta SQL a ejecutar
     * @param array $params Parámetros para consultas preparadas (opcional)
     * @return mixed Resultado de la consulta
     */
    public function executeQuery(string $query, array $params = null) {
        if (!$this->isConnected()) {
            $this->connect();
        }
        
        try {
            // Si hay parámetros, usar consulta preparada
            if ($params !== null && count($params) > 0) {
                return $this->executePrepared($query, $params);
            }
            
            // Consulta simple
            $result = $this->connection->query($query);
            
            if ($result === false) {
                throw new Exception("Error en la consulta: " . $this->connection->error);
            }
            
            // Para consultas SELECT, devolver array de resultados
            if ($result instanceof mysqli_result) {
                $data = [];
                while ($row = $result->fetch_assoc()) {
                    $data[] = $row;
                }
                $result->free();
                return $data;
            }
            
            // Para INSERT, UPDATE, DELETE devolver filas afectadas
            return $this->connection->affected_rows;
            
        } catch (Exception $e) {
            echo "❌ Error ejecutando consulta: " . $e->getMessage() . "\n";
            echo "📋 Query: $query\n";
            return null;
        }
    }
    
    /**
     * Ejecuta una consulta preparada (prepared statement)
     * 
     * @param string $query Consulta con placeholders (?)
     * @param array $params Parámetros a vincular
     * @return mixed Resultado de la consulta
     */
    private function executePrepared(string $query, array $params) {
        $stmt = $this->connection->prepare($query);
        
        if ($stmt === false) {
            throw new Exception("Error preparando consulta: " . $this->connection->error);
        }
        
        // Detectar tipos de parámetros
        $types = '';
        foreach ($params as $param) {
            if (is_int($param)) {
                $types .= 'i';
            } elseif (is_float($param)) {
                $types .= 'd';
            } else {
                $types .= 's';
            }
        }
        
        // Vincular parámetros
        $stmt->bind_param($types, ...$params);
        
        // Ejecutar
        $stmt->execute();
        
        // Obtener resultados
        $result = $stmt->get_result();
        
        if ($result instanceof mysqli_result) {
            $data = [];
            while ($row = $result->fetch_assoc()) {
                $data[] = $row;
            }
            $stmt->close();
            return $data;
        }
        
        $affected = $stmt->affected_rows;
        $stmt->close();
        return $affected;
    }
    
    /**
     * Obtiene la lista de tablas en la base de datos
     * 
     * @return array Lista de nombres de tablas
     */
    public function getTables(): array {
        $result = $this->executeQuery("SHOW TABLES");
        if ($result) {
            return array_map(fn($row) => array_values($row)[0], $result);
        }
        return [];
    }
    
    /**
     * Obtiene información sobre las columnas de una tabla
     * 
     * @param string $tableName Nombre de la tabla
     * @return array Información de las columnas
     */
    public function getTableInfo(string $tableName): array {
        return $this->executeQuery("DESCRIBE $tableName") ?? [];
    }
    
    /**
     * Obtiene el ID del último registro insertado
     * 
     * @return int ID del último insert
     */
    public function getLastInsertId(): int {
        return $this->connection->insert_id;
    }
    
    /**
     * Escapa una cadena para prevenir SQL injection
     * 
     * @param string $string Cadena a escapar
     * @return string Cadena escapada
     */
    public function escapeString(string $string): string {
        if (!$this->isConnected()) {
            $this->connect();
        }
        return $this->connection->real_escape_string($string);
    }
    
    /**
     * Inicia una transacción
     */
    public function beginTransaction(): void {
        $this->connection->begin_transaction();
    }
    
    /**
     * Confirma una transacción
     */
    public function commit(): void {
        $this->connection->commit();
    }
    
    /**
     * Revierte una transacción
     */
    public function rollback(): void {
        $this->connection->rollback();
    }
    
    /**
     * Destructor - Cierra la conexión automáticamente
     */
    public function __destruct() {
        $this->disconnect();
    }
}


/**
 * Constructor de consultas SQL de forma programática
 */
class YourSQLQueryBuilder {
    private YourSQLConnection $connection;
    private string $select = '*';
    private string $from = '';
    private array $where = [];
    private array $orderBy = [];
    private ?int $limit = null;
    private ?int $offset = null;
    
    /**
     * Constructor
     * 
     * @param YourSQLConnection $connection Conexión a la base de datos
     */
    public function __construct(YourSQLConnection $connection) {
        $this->connection = $connection;
    }
    
    /**
     * Reinicia el estado del query builder
     * 
     * @return self
     */
    public function reset(): self {
        $this->select = '*';
        $this->from = '';
        $this->where = [];
        $this->orderBy = [];
        $this->limit = null;
        $this->offset = null;
        return $this;
    }
    
    /**
     * Define las columnas a seleccionar
     * 
     * @param string ...$columns Columnas a seleccionar
     * @return self
     */
    public function select(string ...$columns): self {
        $this->select = count($columns) > 0 ? implode(', ', $columns) : '*';
        return $this;
    }
    
    /**
     * Define la tabla principal
     * 
     * @param string $table Nombre de la tabla
     * @return self
     */
    public function from(string $table): self {
        $this->from = $table;
        return $this;
    }
    
    /**
     * Añade una condición WHERE
     * 
     * @param string $condition Condición WHERE
     * @return self
     */
    public function where(string $condition): self {
        $this->where[] = $condition;
        return $this;
    }
    
    /**
     * Añade ORDER BY
     * 
     * @param string $column Columna para ordenar
     * @param string $direction Dirección (ASC o DESC)
     * @return self
     */
    public function orderBy(string $column, string $direction = 'ASC'): self {
        $this->orderBy[] = "$column $direction";
        return $this;
    }
    
    /**
     * Añade LIMIT
     * 
     * @param int $limit Número de registros
     * @return self
     */
    public function limit(int $limit): self {
        $this->limit = $limit;
        return $this;
    }
    
    /**
     * Añade OFFSET
     * 
     * @param int $offset Desplazamiento
     * @return self
     */
    public function offset(int $offset): self {
        $this->offset = $offset;
        return $this;
    }
    
    /**
     * Construye la consulta SQL
     * 
     * @return string Consulta SQL construida
     */
    public function build(): string {
        $query = "SELECT {$this->select} FROM {$this->from}";
        
        if (count($this->where) > 0) {
            $query .= ' WHERE ' . implode(' AND ', $this->where);
        }
        
        if (count($this->orderBy) > 0) {
            $query .= ' ORDER BY ' . implode(', ', $this->orderBy);
        }
        
        if ($this->limit !== null) {
            $query .= " LIMIT {$this->limit}";
        }
        
        if ($this->offset !== null) {
            $query .= " OFFSET {$this->offset}";
        }
        
        return $query;
    }
    
    /**
     * Ejecuta la consulta construida
     * 
     * @return mixed Resultado de la consulta
     */
    public function execute() {
        $query = $this->build();
        $result = $this->connection->executeQuery($query);
        $this->reset();
        return $result;
    }
}
