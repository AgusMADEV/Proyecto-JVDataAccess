"""
JVDB 2.0 - Clase de Abstracción para Acceso a Base de Datos
Versión: 2.0.0

Versión mejorada con:
- Sistema de logging integrado
- Pool de conexiones
- Soporte para transacciones
- CRUD completo optimizado
- Manejo robusto de errores
"""

import json
from typing import Optional, List, Dict, Any, Union
from contextlib import contextmanager

try:
    # Importaciones relativas (cuando se usa como paquete)
    from ..yoursql import YourSQLConnection
    from .connection_pool import JVConnectionPool, PooledConnection
    from .logger import JVLogger
    from .exceptions import *
except ImportError:
    # Importaciones absolutas (cuando se ejecuta directamente)
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from yoursql.yoursql import YourSQLConnection
    from jvdb.connection_pool import JVConnectionPool, PooledConnection
    from jvdb.logger import JVLogger
    from jvdb.exceptions import *


class JVDB2:
    """
    Clase de abstracción mejorada para acceso a base de datos MySQL
    Versión 2.0 con pool de conexiones, logging y transacciones
    """
    
    def __init__(
        self,
        host: str,
        usuario: str,
        contrasena: str,
        basedatos: str,
        port: int = 3306,
        use_pool: bool = True,
        pool_config: Optional[Dict] = None,
        log_config: Optional[Dict] = None
    ):
        """
        Inicializa JVDB2 con los parámetros de conexión
        
        Args:
            host: Dirección del servidor MySQL
            usuario: Usuario de la base de datos
            contrasena: Contraseña del usuario
            basedatos: Nombre de la base de datos
            port: Puerto de conexión (por defecto 3306)
            use_pool: Usar pool de conexiones (por defecto True)
            pool_config: Configuración del pool
            log_config: Configuración del logger
        """
        self.host = host
        self.usuario = usuario
        self.contrasena = contrasena
        self.basedatos = basedatos
        self.port = port
        
        # Configurar logger
        log_cfg = log_config or {}
        self.logger = JVLogger.get_instance("JVDB2", **log_cfg)
        
        # Pool de conexiones o conexión simple
        self.use_pool = use_pool
        self.pool = None
        self.conexion = None
        
        if use_pool:
            pool_cfg = pool_config or {}
            self.pool = JVConnectionPool(
                host=host,
                user=usuario,
                password=contrasena,
                database=basedatos,
                port=port,
                min_size=pool_cfg.get('min_size', 2),
                max_size=pool_cfg.get('max_size', 10),
                max_lifetime=pool_cfg.get('max_lifetime', 3600),
                timeout=pool_cfg.get('timeout', 30),
                logger=self.logger
            )
            self.logger.info(f"JVDB2 inicializado con pool de conexiones")
        else:
            self.conexion = YourSQLConnection(
                host=host,
                user=usuario,
                password=contrasena,
                database=basedatos,
                port=port
            )
            if self.conexion.connect():
                self.logger.connection(host, basedatos, True)
            else:
                self.logger.connection(host, basedatos, False)
                raise ConnectionError(f"No se pudo conectar a {host}/{basedatos}")
    
    @contextmanager
    def _get_connection(self):
        """Context manager para obtener una conexión"""
        if self.use_pool:
            pooled_conn = self.pool.acquire()
            try:
                yield pooled_conn.connection
            finally:
                self.pool.release(pooled_conn)
        else:
            yield self.conexion
    
    def seleccionar(
        self,
        tabla: str,
        columnas: Union[str, List[str]] = "*",
        where: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        formato: str = "list"
    ) -> Union[str, List[Dict]]:
        """
        Selecciona registros de una tabla con opciones avanzadas
        
        Args:
            tabla: Nombre de la tabla
            columnas: Columnas a seleccionar (lista o string)
            where: Condiciones WHERE como diccionario
            order_by: Ordenamiento (ej: "columna DESC")
            limit: Límite de resultados
            offset: Offset para paginación
            formato: 'json' o 'list' (por defecto list)
            
        Returns:
            Datos en el formato especificado
        """
        try:
            # Construir columnas
            if isinstance(columnas, list):
                cols = ", ".join(columnas)
            else:
                cols = columnas
            
            # Construir query
            query = f"SELECT {cols} FROM {tabla}"
            params = []
            
            # Agregar WHERE
            if where:
                conditions = []
                for col, val in where.items():
                    conditions.append(f"{col} = %s")
                    params.append(val)
                query += " WHERE " + " AND ".join(conditions)
            
            # Agregar ORDER BY
            if order_by:
                query += f" ORDER BY {order_by}"
            
            # Agregar LIMIT y OFFSET
            if limit:
                query += f" LIMIT {limit}"
                if offset:
                    query += f" OFFSET {offset}"
            
            self.logger.query(query, tuple(params) if params else None)
            
            with self._get_connection() as conn:
                resultado = conn.execute_query(
                    query,
                    params=tuple(params) if params else None,
                    fetch_all=True
                )
            
            if resultado is None:
                resultado = []
            
            self.logger.info(f"Seleccionados {len(resultado)} registros de '{tabla}'")
            
            if formato == "json":
                return json.dumps(resultado, ensure_ascii=False, indent=2)
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error en seleccionar: {e}", exc_info=True)
            raise QueryError(f"Error al seleccionar de {tabla}: {e}")
    
    def seleccionar_uno(
        self,
        tabla: str,
        identificador: Optional[int] = None,
        where: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict]:
        """
        Selecciona un único registro
        
        Args:
            tabla: Nombre de la tabla
            identificador: ID del registro (campo Identificador)
            where: Condiciones alternativas como diccionario
            
        Returns:
            Diccionario con el registro o None
        """
        try:
            if identificador is not None:
                where = {'Identificador': identificador}
            elif where is None:
                raise ValidationError("Debe proporcionar identificador o where")
            
            resultados = self.seleccionar(tabla, where=where, limit=1, formato="list")
            return resultados[0] if resultados else None
            
        except Exception as e:
            self.logger.error(f"Error en seleccionar_uno: {e}", exc_info=True)
            raise QueryError(f"Error al seleccionar uno de {tabla}: {e}")
    
    def insertar(
        self,
        tabla: str,
        datos: Dict[str, Any],
        return_id: bool = False
    ) -> Union[int, Dict[str, Any]]:
        """
        Inserta un nuevo registro
        
        Args:
            tabla: Nombre de la tabla
            datos: Diccionario con columna:valor
            return_id: Si True, devuelve dict con rows_affected y last_id
            
        Returns:
            Número de filas afectadas o dict con info
        """
        try:
            if not datos:
                raise ValidationError("No se proporcionaron datos para insertar")
            
            columnas = ", ".join(datos.keys())
            placeholders = ", ".join(["%s"] * len(datos))
            valores = tuple(datos.values())
            
            query = f"INSERT INTO {tabla} ({columnas}) VALUES ({placeholders})"
            self.logger.query(query, valores)
            
            with self._get_connection() as conn:
                resultado = conn.execute_query(query, params=valores)
                last_id = conn._connection.get_server_info() if hasattr(conn, '_connection') else None
            
            self.logger.info(f"Registro insertado en '{tabla}'")
            
            if return_id:
                return {
                    'rows_affected': resultado if resultado else 0,
                    'last_insert_id': last_id
                }
            return resultado if resultado else 0
            
        except Exception as e:
            self.logger.error(f"Error en insertar: {e}", exc_info=True)
            raise QueryError(f"Error al insertar en {tabla}: {e}")
    
    def insertar_multiple(
        self,
        tabla: str,
        registros: List[Dict[str, Any]]
    ) -> int:
        """
        Inserta múltiples registros de forma optimizada
        
        Args:
            tabla: Nombre de la tabla
            registros: Lista de diccionarios con los datos
            
        Returns:
            Número total de filas insertadas
        """
        try:
            if not registros:
                return 0
            
            total = 0
            with self.transaction():
                for registro in registros:
                    total += self.insertar(tabla, registro)
            
            self.logger.info(f"{total} registros insertados en '{tabla}'")
            return total
            
        except Exception as e:
            self.logger.error(f"Error en insertar_multiple: {e}", exc_info=True)
            raise QueryError(f"Error al insertar múltiples en {tabla}: {e}")
    
    def actualizar(
        self,
        tabla: str,
        datos: Dict[str, Any],
        identificador: Optional[int] = None,
        where: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Actualiza registros existentes
        
        Args:
            tabla: Nombre de la tabla
            datos: Diccionario con columna:valor a actualizar
            identificador: ID del registro (campo Identificador)
            where: Condiciones alternativas como diccionario
            
        Returns:
            Número de filas afectadas
        """
        try:
            if not datos:
                raise ValidationError("No se proporcionaron datos para actualizar")
            
            if identificador is not None:
                where = {'Identificador': identificador}
            elif where is None:
                raise ValidationError("Debe proporcionar identificador o where")
            
            # Construir SET clause
            set_clause = ", ".join([f"{col} = %s" for col in datos.keys()])
            valores = list(datos.values())
            
            # Construir WHERE clause
            where_conditions = []
            for col, val in where.items():
                where_conditions.append(f"{col} = %s")
                valores.append(val)
            
            query = f"UPDATE {tabla} SET {set_clause} WHERE " + " AND ".join(where_conditions)
            self.logger.query(query, tuple(valores))
            
            with self._get_connection() as conn:
                resultado = conn.execute_query(query, params=tuple(valores))
            
            self.logger.info(f"{resultado} registro(s) actualizado(s) en '{tabla}'")
            return resultado if resultado else 0
            
        except Exception as e:
            self.logger.error(f"Error en actualizar: {e}", exc_info=True)
            raise QueryError(f"Error al actualizar {tabla}: {e}")
    
    def eliminar(
        self,
        tabla: str,
        identificador: Optional[int] = None,
        where: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Elimina registros de una tabla
        
        Args:
            tabla: Nombre de la tabla
            identificador: ID del registro (campo Identificador)
            where: Condiciones alternativas como diccionario
            
        Returns:
            Número de filas eliminadas
        """
        try:
            if identificador is not None:
                where = {'Identificador': identificador}
            elif where is None:
                raise ValidationError("Debe proporcionar identificador o where")
            
            # Construir WHERE clause
            where_conditions = []
            valores = []
            for col, val in where.items():
                where_conditions.append(f"{col} = %s")
                valores.append(val)
            
            query = f"DELETE FROM {tabla} WHERE " + " AND ".join(where_conditions)
            self.logger.query(query, tuple(valores))
            
            with self._get_connection() as conn:
                resultado = conn.execute_query(query, params=tuple(valores))
            
            self.logger.info(f"{resultado} registro(s) eliminado(s) de '{tabla}'")
            return resultado if resultado else 0
            
        except Exception as e:
            self.logger.error(f"Error en eliminar: {e}", exc_info=True)
            raise QueryError(f"Error al eliminar de {tabla}: {e}")
    
    def contar(
        self,
        tabla: str,
        where: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Cuenta registros en una tabla
        
        Args:
            tabla: Nombre de la tabla
            where: Condiciones opcionales
            
        Returns:
            Número de registros
        """
        try:
            query = f"SELECT COUNT(*) as total FROM {tabla}"
            params = []
            
            if where:
                conditions = []
                for col, val in where.items():
                    conditions.append(f"{col} = %s")
                    params.append(val)
                query += " WHERE " + " AND ".join(conditions)
            
            with self._get_connection() as conn:
                resultado = conn.execute_query(
                    query,
                    params=tuple(params) if params else None,
                    fetch_one=True
                )
            
            return resultado['total'] if resultado else 0
            
        except Exception as e:
            self.logger.error(f"Error en contar: {e}", exc_info=True)
            raise QueryError(f"Error al contar en {tabla}: {e}")
    
    def existe(
        self,
        tabla: str,
        where: Dict[str, Any]
    ) -> bool:
        """
        Verifica si existe al menos un registro que cumpla las condiciones
        
        Args:
            tabla: Nombre de la tabla
            where: Condiciones de búsqueda
            
        Returns:
            True si existe al menos un registro
        """
        return self.contar(tabla, where) > 0
    
    @contextmanager
    def transaction(self):
        """
        Context manager para transacciones
        
        Uso:
            with db.transaction():
                db.insertar('tabla', datos1)
                db.actualizar('tabla', datos2, id=1)
        """
        if not self.use_pool:
            conn = self.conexion
        else:
            pooled_conn = self.pool.acquire()
            conn = pooled_conn.connection
        
        try:
            # Iniciar transacción
            conn._connection.autocommit = False
            self.logger.transaction("BEGIN")
            
            yield conn
            
            # Commit
            conn._connection.commit()
            self.logger.transaction("COMMIT")
            
        except Exception as e:
            # Rollback
            conn._connection.rollback()
            self.logger.transaction("ROLLBACK")
            self.logger.error(f"Error en transacción: {e}", exc_info=True)
            raise TransactionError(f"Error en transacción: {e}")
        
        finally:
            conn._connection.autocommit = True
            if self.use_pool:
                self.pool.release(pooled_conn)
    
    def consulta_personalizada(
        self,
        query: str,
        params: Optional[tuple] = None,
        fetch: str = "all"
    ) -> Any:
        """
        Ejecuta una consulta SQL personalizada
        
        Args:
            query: Consulta SQL
            params: Parámetros para consultas preparadas
            fetch: 'all', 'one', o 'none'
            
        Returns:
            Resultados según el tipo de consulta
        """
        try:
            self.logger.query(query, params)
            
            with self._get_connection() as conn:
                if fetch == "one":
                    resultado = conn.execute_query(query, params=params, fetch_one=True)
                elif fetch == "all":
                    resultado = conn.execute_query(query, params=params, fetch_all=True)
                else:
                    resultado = conn.execute_query(query, params=params)
            
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error en consulta personalizada: {e}", exc_info=True)
            raise QueryError(f"Error en consulta: {e}")
    
    def get_pool_stats(self) -> Optional[Dict[str, Any]]:
        """Obtiene estadísticas del pool de conexiones"""
        if self.pool:
            return self.pool.get_stats()
        return None
    
    def cerrar(self):
        """Cierra el pool o la conexión"""
        try:
            if self.pool:
                self.pool.close()
                self.logger.info("Pool de conexiones cerrado")
            elif self.conexion:
                self.conexion.disconnect()
                self.logger.info("Conexión cerrada")
        except Exception as e:
            self.logger.error(f"Error al cerrar: {e}")
    
    def __enter__(self):
        """Soporte para context manager"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra al salir del contexto"""
        self.cerrar()
    
    def __del__(self):
        """Destructor"""
        try:
            self.cerrar()
        except:
            pass
