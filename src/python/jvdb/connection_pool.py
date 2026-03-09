"""
JVConnectionPool - Pool de Conexiones para YourSQL
Versión: 2.0.0

Gestiona un pool de conexiones reutilizables para mejorar el rendimiento
"""

from queue import Queue, Empty
from threading import Lock
from typing import Optional, Dict, Any
import time

try:
    # Importaciones relativas (cuando se usa como paquete)
    from ..yoursql import YourSQLConnection
    from .exceptions import PoolExhaustedError, ConnectionError as JVConnectionError
    from .logger import JVLogger
except ImportError:
    # Importaciones absolutas (cuando se ejecuta directamente)
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from yoursql.yoursql import YourSQLConnection
    from jvdb.exceptions import PoolExhaustedError, ConnectionError as JVConnectionError
    from jvdb.logger import JVLogger


class PooledConnection:
    """Envoltorio para una conexión del pool"""
    
    def __init__(self, connection: YourSQLConnection, pool: 'JVConnectionPool'):
        self.connection = connection
        self.pool = pool
        self.in_use = False
        self.created_at = time.time()
        self.last_used = time.time()
    
    def __enter__(self):
        """Context manager entry"""
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - devuelve la conexión al pool"""
        self.pool.release(self)


class JVConnectionPool:
    """
    Pool de conexiones MySQL con gestión automática
    """
    
    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        database: str,
        port: int = 3306,
        min_size: int = 2,
        max_size: int = 10,
        max_lifetime: int = 3600,
        timeout: int = 30,
        logger: Optional[JVLogger] = None
    ):
        """
        Inicializa el pool de conexiones
        
        Args:
            host: Host del servidor MySQL
            user: Usuario de la base de datos
            password: Contraseña del usuario
            database: Nombre de la base de datos
            port: Puerto de conexión
            min_size: Número mínimo de conexiones en el pool
            max_size: Número máximo de conexiones en el pool
            max_lifetime: Tiempo máximo de vida de una conexión (segundos)
            timeout: Tiempo máximo de espera para obtener una conexión
            logger: Logger para registrar eventos
        """
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': port
        }
        
        self.min_size = min_size
        self.max_size = max_size
        self.max_lifetime = max_lifetime
        self.timeout = timeout
        
        self.logger = logger or JVLogger.get_instance("JVPool")
        
        self._pool: Queue = Queue(maxsize=max_size)
        self._connections: list[PooledConnection] = []
        self._lock = Lock()
        self._closed = False
        
        # Crear conexiones mínimas
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Crea las conexiones mínimas del pool"""
        self.logger.info(f"Inicializando pool con {self.min_size} conexiones")
        
        for _ in range(self.min_size):
            try:
                conn = self._create_connection()
                self._pool.put(conn)
            except Exception as e:
                self.logger.error(f"Error al crear conexión inicial: {e}")
    
    def _create_connection(self) -> PooledConnection:
        """Crea una nueva conexión"""
        try:
            connection = YourSQLConnection(**self.config)
            if not connection.connect():
                raise JVConnectionError("No se pudo establecer la conexión")
            
            pooled_conn = PooledConnection(connection, self)
            
            with self._lock:
                self._connections.append(pooled_conn)
            
            self.logger.debug(f"Nueva conexión creada. Total: {len(self._connections)}")
            return pooled_conn
            
        except Exception as e:
            self.logger.error(f"Error al crear conexión: {e}")
            raise JVConnectionError(f"Error al crear conexión: {e}")
    
    def acquire(self) -> PooledConnection:
        """
        Obtiene una conexión del pool
        
        Returns:
            PooledConnection: Conexión lista para usar
            
        Raises:
            PoolExhaustedError: Si no hay conexiones disponibles
        """
        if self._closed:
            raise JVConnectionError("El pool está cerrado")
        
        start_time = time.time()
        
        while True:
            try:
                # Intentar obtener una conexión del pool
                pooled_conn = self._pool.get(timeout=1)
                
                # Verificar si la conexión es válida
                if self._is_valid(pooled_conn):
                    pooled_conn.in_use = True
                    pooled_conn.last_used = time.time()
                    self.logger.debug("Conexión obtenida del pool")
                    return pooled_conn
                else:
                    # Conexión inválida, crear una nueva
                    self.logger.warning("Conexión inválida, creando nueva")
                    self._remove_connection(pooled_conn)
                    
            except Empty:
                # No hay conexiones disponibles
                if len(self._connections) < self.max_size:
                    # Crear nueva conexión
                    self.logger.info("Pool vacío, creando nueva conexión")
                    pooled_conn = self._create_connection()
                    pooled_conn.in_use = True
                    return pooled_conn
                
                # Verificar timeout
                if time.time() - start_time > self.timeout:
                    raise PoolExhaustedError(
                        f"No se pudo obtener conexión en {self.timeout} segundos"
                    )
    
    def release(self, pooled_conn: PooledConnection):
        """
        Devuelve una conexión al pool
        
        Args:
            pooled_conn: Conexión a devolver
        """
        if self._closed:
            return
        
        pooled_conn.in_use = False
        pooled_conn.last_used = time.time()
        
        # Verificar si la conexión debe ser cerrada por edad
        if time.time() - pooled_conn.created_at > self.max_lifetime:
            self.logger.info("Conexión expirada, cerrando")
            self._remove_connection(pooled_conn)
            
            # Crear una nueva si estamos por debajo del mínimo
            if len(self._connections) < self.min_size:
                new_conn = self._create_connection()
                self._pool.put(new_conn)
        else:
            self._pool.put(pooled_conn)
            self.logger.debug("Conexión devuelta al pool")
    
    def _is_valid(self, pooled_conn: PooledConnection) -> bool:
        """Verifica si una conexión es válida"""
        try:
            return pooled_conn.connection.is_connected()
        except:
            return False
    
    def _remove_connection(self, pooled_conn: PooledConnection):
        """Elimina una conexión del pool"""
        try:
            pooled_conn.connection.disconnect()
        except:
            pass
        
        with self._lock:
            if pooled_conn in self._connections:
                self._connections.remove(pooled_conn)
        
        self.logger.debug(f"Conexión eliminada. Total: {len(self._connections)}")
    
    def close(self):
        """Cierra todas las conexiones del pool"""
        self.logger.info("Cerrando pool de conexiones")
        self._closed = True
        
        # Vaciar la cola
        while not self._pool.empty():
            try:
                self._pool.get_nowait()
            except Empty:
                break
        
        # Cerrar todas las conexiones
        with self._lock:
            for pooled_conn in self._connections[:]:
                try:
                    pooled_conn.connection.disconnect()
                except:
                    pass
            self._connections.clear()
        
        self.logger.info("Pool cerrado")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del pool
        
        Returns:
            Diccionario con estadísticas
        """
        with self._lock:
            total = len(self._connections)
            in_use = sum(1 for c in self._connections if c.in_use)
            available = total - in_use
        
        return {
            'total_connections': total,
            'in_use': in_use,
            'available': available,
            'min_size': self.min_size,
            'max_size': self.max_size,
            'is_closed': self._closed
        }
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
