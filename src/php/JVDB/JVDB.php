<?php
/**
 * JVDB - Clase de Abstracción para Acceso a Base de Datos (PHP)
 * Versión: 1.0.0
 * 
 * Proporciona una interfaz simplificada para operaciones comunes
 * de base de datos utilizando YourSQL como backend.
 */

namespace JVDB;

require_once __DIR__ . '/../YourSQL/YourSQL.php';

use YourSQL\YourSQLConnection;

class JVDB {
    private string $host;
    private string $usuario;
    private string $contrasena;
    private string $basedatos;
    private int $port;
    private YourSQLConnection $conexion;
    
    /**
     * Constructor - Inicializa JVDB con los parámetros de conexión
     * 
     * @param string $host Dirección del servidor MySQL
     * @param string $usuario Usuario de la base de datos
     * @param string $contrasena Contraseña del usuario
     * @param string $basedatos Nombre de la base de datos
     * @param int $port Puerto de conexión (por defecto 3306)
     * @param bool $autoconnect Conectar automáticamente (por defecto true)
     */
    public function __construct(
        string $host,
        string $usuario,
        string $contrasena,
        string $basedatos,
        int $port = 3306,
        bool $autoconnect = true
    ) {
        $this->host = $host;
        $this->usuario = $usuario;
        $this->contrasena = $contrasena;
        $this->basedatos = $basedatos;
        $this->port = $port;
        
        // Crear conexión usando YourSQL
        $this->conexion = new YourSQLConnection(
            $host,
            $usuario,
            $contrasena,
            $basedatos,
            $port
        );
        
        if ($autoconnect) {
            $this->conectar();
        }
    }
    
    /**
     * Establece la conexión con la base de datos
     * 
     * @return bool True si la conexión fue exitosa
     */
    public function conectar(): bool {
        $resultado = $this->conexion->connect();
        if ($resultado) {
            echo "✅ Conectado a la base de datos '{$this->basedatos}'\n";
        }
        return $resultado;
    }
    
    /**
     * Cierra la conexión con la base de datos
     */
    public function desconectar(): void {
        $this->conexion->disconnect();
        echo "🔌 Conexión cerrada\n";
    }
    
    /**
     * Verifica si hay conexión activa
     * 
     * @return bool True si está conectado
     */
    public function estaConectado(): bool {
        return $this->conexion->isConnected();
    }
    
    /**
     * Selecciona todos los registros de una tabla
     * 
     * @param string $tabla Nombre de la tabla
     * @param string $columnas Columnas a seleccionar (por defecto todas)
     * @param string $formato 'json' o 'array' (por defecto json)
     * @return string|array Datos en el formato especificado
     */
    public function seleccionar(
        string $tabla,
        string $columnas = '*',
        string $formato = 'json'
    ) {
        $query = "SELECT $columnas FROM $tabla";
        $resultado = $this->conexion->executeQuery($query);
        
        if ($resultado === null) {
            $resultado = [];
        }
        
        if ($formato === 'json') {
            return json_encode($resultado, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        }
        
        return $resultado;
    }
    
    /**
     * Selecciona un único registro por su identificador
     * 
     * @param string $tabla Nombre de la tabla
     * @param int $identificador ID del registro
     * @return array|null Diccionario con el registro o null
     */
    public function seleccionarUno(string $tabla, int $identificador): ?array {
        $query = "SELECT * FROM $tabla WHERE Identificador = ?";
        $resultado = $this->conexion->executeQuery($query, [$identificador]);
        
        return count($resultado) > 0 ? $resultado[0] : null;
    }
    
    /**
     * Busca registros por un criterio específico
     * 
     * @param string $tabla Nombre de la tabla
     * @param string $columna Columna donde buscar
     * @param mixed $valor Valor a buscar
     * @param string $formato 'json' o 'array'
     * @return string|array Resultados en el formato especificado
     */
    public function buscar(
        string $tabla,
        string $columna,
        $valor,
        string $formato = 'json'
    ) {
        $query = "SELECT * FROM $tabla WHERE $columna LIKE ?";
        $likeValor = "%$valor%";
        $resultado = $this->conexion->executeQuery($query, [$likeValor]);
        
        if ($resultado === null) {
            $resultado = [];
        }
        
        if ($formato === 'json') {
            return json_encode($resultado, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        }
        
        return $resultado;
    }
    
    /**
     * Inserta un nuevo registro en una tabla
     * 
     * @param string $tabla Nombre de la tabla
     * @param array $datos Array asociativo con columna => valor
     * @return int Número de filas afectadas
     */
    public function insertar(string $tabla, array $datos): int {
        $columnas = implode(', ', array_keys($datos));
        $placeholders = implode(', ', array_fill(0, count($datos), '?'));
        $valores = array_values($datos);
        
        $query = "INSERT INTO $tabla ($columnas) VALUES ($placeholders)";
        $resultado = $this->conexion->executeQuery($query, $valores);
        
        if ($resultado && $resultado > 0) {
            echo "✅ Registro insertado en '$tabla'\n";
        }
        
        return $resultado ?? 0;
    }
    
    /**
     * Actualiza un registro existente
     * 
     * @param string $tabla Nombre de la tabla
     * @param int $identificador ID del registro a actualizar
     * @param array $datos Array asociativo con columna => valor
     * @return int Número de filas afectadas
     */
    public function actualizar(string $tabla, int $identificador, array $datos): int {
        $setClause = implode(', ', array_map(
            fn($col) => "$col = ?",
            array_keys($datos)
        ));
        
        $valores = array_merge(array_values($datos), [$identificador]);
        
        $query = "UPDATE $tabla SET $setClause WHERE Identificador = ?";
        $resultado = $this->conexion->executeQuery($query, $valores);
        
        if ($resultado && $resultado > 0) {
            echo "✅ Registro actualizado en '$tabla'\n";
        }
        
        return $resultado ?? 0;
    }
    
    /**
     * Elimina un registro de una tabla
     * 
     * @param string $tabla Nombre de la tabla
     * @param int $identificador ID del registro a eliminar
     * @return int Número de filas afectadas
     */
    public function eliminar(string $tabla, int $identificador): int {
        $query = "DELETE FROM $tabla WHERE Identificador = ?";
        $resultado = $this->conexion->executeQuery($query, [$identificador]);
        
        if ($resultado && $resultado > 0) {
            echo "✅ Registro eliminado de '$tabla'\n";
        }
        
        return $resultado ?? 0;
    }
    
    /**
     * Lista todas las tablas de la base de datos
     * 
     * @param string $formato 'json' o 'array'
     * @return string|array Lista de tablas en el formato especificado
     */
    public function tablas(string $formato = 'json') {
        $resultado = $this->conexion->getTables();
        
        if ($formato === 'json') {
            return json_encode($resultado, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        }
        
        return $resultado;
    }
    
    /**
     * Obtiene la estructura de una tabla
     * 
     * @param string $tabla Nombre de la tabla
     * @param string $formato 'json' o 'array'
     * @return string|array Información de las columnas
     */
    public function estructuraTabla(string $tabla, string $formato = 'json') {
        $resultado = $this->conexion->getTableInfo($tabla);
        
        if ($formato === 'json') {
            return json_encode($resultado, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        }
        
        return $resultado;
    }
    
    /**
     * Ejecuta una consulta SQL personalizada
     * 
     * @param string $query Consulta SQL
     * @param array|null $params Parámetros para consultas preparadas
     * @param string $formato 'json' o 'array'
     * @return string|array|int Resultados de la consulta
     */
    public function consultaPersonalizada(
        string $query,
        ?array $params = null,
        string $formato = 'json'
    ) {
        $esSelect = stripos(trim($query), 'SELECT') === 0;
        
        if ($esSelect) {
            $resultado = $this->conexion->executeQuery($query, $params);
            if ($resultado === null) {
                $resultado = [];
            }
            
            if ($formato === 'json') {
                return json_encode($resultado, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
            }
            
            return $resultado;
        } else {
            // Para INSERT, UPDATE, DELETE
            return $this->conexion->executeQuery($query, $params) ?? 0;
        }
    }
    
    /**
     * Obtiene el ID del último registro insertado
     * 
     * @return int ID del último insert
     */
    public function ultimoIdInsertado(): int {
        return $this->conexion->getLastInsertId();
    }
    
    /**
     * Inicia una transacción
     */
    public function iniciarTransaccion(): void {
        $this->conexion->beginTransaction();
        echo "🔄 Transacción iniciada\n";
    }
    
    /**
     * Confirma una transacción
     */
    public function confirmarTransaccion(): void {
        $this->conexion->commit();
        echo "✅ Transacción confirmada\n";
    }
    
    /**
     * Revierte una transacción
     */
    public function revertirTransaccion(): void {
        $this->conexion->rollback();
        echo "↩️  Transacción revertida\n";
    }
    
    /**
     * Destructor - Asegura que la conexión se cierre
     */
    public function __destruct() {
        if ($this->conexion && $this->estaConectado()) {
            $this->desconectar();
        }
    }
}
