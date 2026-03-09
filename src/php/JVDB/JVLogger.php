<?php
/**
 * JVLogger - Sistema de Logging para JVDataAccess (PHP)
 * Versión: 2.0.0
 * 
 * Sistema de registro de eventos y operaciones de base de datos
 */

namespace JVDB;

class JVLogger {
    private string $name;
    private string $logDir;
    private int $logLevel;
    private bool $consoleOutput;
    private bool $fileOutput;
    private ?string $logFile = null;
    
    // Niveles de log
    const DEBUG = 100;
    const INFO = 200;
    const WARNING = 300;
    const ERROR = 400;
    const CRITICAL = 500;
    
    private static array $instances = [];
    
    /**
     * Constructor del logger
     * 
     * @param string $name Nombre del logger
     * @param string $logDir Directorio donde guardar los logs
     * @param int $logLevel Nivel de logging
     * @param bool $consoleOutput Mostrar logs en consola
     * @param bool $fileOutput Guardar logs en archivo
     */
    public function __construct(
        string $name = 'JVDB',
        string $logDir = 'logs',
        int $logLevel = self::INFO,
        bool $consoleOutput = true,
        bool $fileOutput = true
    ) {
        $this->name = $name;
        $this->logDir = $logDir;
        $this->logLevel = $logLevel;
        $this->consoleOutput = $consoleOutput;
        $this->fileOutput = $fileOutput;
        
        // Crear directorio de logs si no existe
        if ($fileOutput && !is_dir($logDir)) {
            mkdir($logDir, 0777, true);
        }
        
        // Definir archivo de log
        if ($fileOutput) {
            $fecha = date('Y-m-d');
            $this->logFile = "$logDir/{$name}_{$fecha}.log";
        }
    }
    
    /**
     * Obtiene una instancia singleton del logger
     * 
     * @param string $name Nombre del logger
     * @param array $config Configuración adicional
     * @return JVLogger Instancia del logger
     */
    public static function getInstance(string $name = 'JVDB', array $config = []): JVLogger {
        if (!isset(self::$instances[$name])) {
            self::$instances[$name] = new self(
                $name,
                $config['log_dir'] ?? 'logs',
                $config['log_level'] ?? self::INFO,
                $config['console_output'] ?? true,
                $config['file_output'] ?? true
            );
        }
        return self::$instances[$name];
    }
    
    /**
     * Registra un mensaje con un nivel específico
     * 
     * @param int $level Nivel del mensaje
     * @param string $levelName Nombre del nivel
     * @param string $mensaje Mensaje a registrar
     */
    private function log(int $level, string $levelName, string $mensaje): void {
        if ($level < $this->logLevel) {
            return;
        }
        
        $timestamp = date('Y-m-d H:i:s');
        $logMessage = "$timestamp - {$this->name} - $levelName - $mensaje\n";
        
        // Escribir en consola
        if ($this->consoleOutput) {
            echo $logMessage;
        }
        
        // Escribir en archivo
        if ($this->fileOutput && $this->logFile) {
            file_put_contents($this->logFile, $logMessage, FILE_APPEND);
        }
    }
    
    /**
     * Registra un mensaje de debug
     */
    public function debug(string $mensaje): void {
        $this->log(self::DEBUG, 'DEBUG', $mensaje);
    }
    
    /**
     * Registra un mensaje informativo
     */
    public function info(string $mensaje): void {
        $this->log(self::INFO, 'INFO', $mensaje);
    }
    
    /**
     * Registra una advertencia
     */
    public function warning(string $mensaje): void {
        $this->log(self::WARNING, 'WARNING', $mensaje);
    }
    
    /**
     * Registra un error
     */
    public function error(string $mensaje): void {
        $this->log(self::ERROR, 'ERROR', $mensaje);
    }
    
    /**
     * Registra un error crítico
     */
    public function critical(string $mensaje): void {
        $this->log(self::CRITICAL, 'CRITICAL', $mensaje);
    }
    
    /**
     * Registra una consulta SQL
     * 
     * @param string $query Consulta SQL
     * @param array|null $params Parámetros de la consulta
     */
    public function query(string $query, ?array $params = null): void {
        if ($params) {
            $paramsStr = json_encode($params);
            $this->info("SQL: $query | Params: $paramsStr");
        } else {
            $this->info("SQL: $query");
        }
    }
    
    /**
     * Registra un intento de conexión
     * 
     * @param string $host Host de la base de datos
     * @param string $database Nombre de la base de datos
     * @param bool $success Si la conexión fue exitosa
     */
    public function connection(string $host, string $database, bool $success = true): void {
        if ($success) {
            $this->info("Conexión exitosa a $host/$database");
        } else {
            $this->error("Error al conectar a $host/$database");
        }
    }
    
    /**
     * Registra una operación de transacción
     * 
     * @param string $action Acción realizada (BEGIN, COMMIT, ROLLBACK)
     */
    public function transaction(string $action): void {
        $this->info("Transacción: $action");
    }
    
    /**
     * Cambia el nivel de logging
     * 
     * @param int $level Nuevo nivel
     */
    public function setLevel(int $level): void {
        $this->logLevel = $level;
    }
}
