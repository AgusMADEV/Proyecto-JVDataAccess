"""
YourSQL - Conector MySQL Personalizado
Versión: 1.0.0

Este módulo proporciona una capa de abstracción sobre mysql.connector
con funcionalidades adicionales y una interfaz más intuitiva.
"""

import mysql.connector
from mysql.connector import Error
from typing import Optional, Dict, Any, List, Tuple
import json


class YourSQLConnection:
    """
    Clase para gestionar conexiones a MySQL con funcionalidades mejoradas
    """
    
    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        database: str,
        port: int = 3306,
        charset: str = 'utf8mb4',
        autocommit: bool = True
    ):
        """
        Inicializa una conexión a MySQL
        
        Args:
            host: Dirección del servidor MySQL
            user: Usuario de la base de datos
            password: Contraseña del usuario
            database: Nombre de la base de datos
            port: Puerto de conexión (por defecto 3306)
            charset: Codificación de caracteres (por defecto utf8mb4)
            autocommit: Auto-commit de transacciones (por defecto True)
        """
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': port,
            'charset': charset,
            'autocommit': autocommit
        }
        
        self._connection: Optional[mysql.connector.MySQLConnection] = None
        self._cursor = None
        self._connected = False
        
    def connect(self) -> bool:
        """
        Establece la conexión con la base de datos
        
        Returns:
            bool: True si la conexión fue exitosa, False en caso contrario
        """
        try:
            self._connection = mysql.connector.connect(**self.config)
            self._connected = True
            return True
        except Error as e:
            print(f"❌ Error al conectar con MySQL: {e}")
            self._connected = False
            return False
    
    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        try:
            if self._cursor:
                self._cursor.close()
        except:
            pass
        
        try:
            if self._connection:
                # Consumir resultados pendientes antes de cerrar
                if hasattr(self._connection, 'unread_result') and self._connection.unread_result:
                    self._connection.consume_results()
                    
                if self._connection.is_connected():
                    self._connection.close()
                    
            self._connected = False
        except:
            self._connected = False
            
    def is_connected(self) -> bool:
        """
        Verifica si la conexión está activa
        
        Returns:
            bool: True si hay conexión activa
        """
        return self._connected and self._connection and self._connection.is_connected()
    
    def get_cursor(self, dictionary: bool = True, buffered: bool = True):
        """
        Obtiene un cursor para ejecutar consultas
        
        Args:
            dictionary: Si True, devuelve resultados como diccionarios
            buffered: Si True, consume todos los resultados inmediatamente (recomendado)
            
        Returns:
            Cursor de MySQL
        """
        if not self.is_connected():
            self.connect()
            
        return self._connection.cursor(dictionary=dictionary, buffered=buffered)
    
    def execute_query(
        self,
        query: str,
        params: Optional[Tuple] = None,
        fetch_one: bool = False,
        fetch_all: bool = True
    ) -> Optional[Any]:
        """
        Ejecuta una consulta SQL
        
        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para consultas preparadas
            fetch_one: Si True, devuelve solo un resultado
            fetch_all: Si True, devuelve todos los resultados
            
        Returns:
            Resultados de la consulta o None
        """
        cursor = self.get_cursor(buffered=True)
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Detectar tipo de consulta
            query_upper = query.strip().upper()
            
            # Para consultas que devuelven resultados (SELECT, SHOW, DESCRIBE, etc.)
            if any(query_upper.startswith(cmd) for cmd in ['SELECT', 'SHOW', 'DESCRIBE', 'EXPLAIN']):
                if fetch_one:
                    result = cursor.fetchone()
                    return result
                elif fetch_all:
                    result = cursor.fetchall()
                    return result
                else:
                    return None
            
            # Para INSERT, UPDATE, DELETE
            self._connection.commit()
            return cursor.rowcount
            
        except Error as e:
            print(f"❌ Error ejecutando consulta: {e}")
            print(f"📋 Query: {query}")
            if params:
                print(f"📋 Params: {params}")
            return None
        finally:
            try:
                cursor.close()
            except:
                pass  # Ignorar errores al cerrar el cursor
    
    def execute_many(self, query: str, data: List[Tuple]) -> int:
        """
        Ejecuta una consulta múltiples veces con diferentes datos
        
        Args:
            query: Consulta SQL con placeholders
            data: Lista de tuplas con los datos
            
        Returns:
            int: Número de filas afectadas
        """
        cursor = self.get_cursor(dictionary=False, buffered=True)
        
        try:
            cursor.executemany(query, data)
            self._connection.commit()
            return cursor.rowcount
        except Error as e:
            print(f"❌ Error en execute_many: {e}")
            return 0
        finally:
            try:
                cursor.close()
            except:
                passcursor(dictionary=False)
        
        try:
            cursor.executemany(query, data)
            self._connection.commit()
            return cursor.rowcount
        except Error as e:
            print(f"❌ Error en execute_many: {e}")
            return 0
        finally:
            cursor.close()
    
    def get_tables(self) -> List[str]:
        """
        Obtiene la lista de tablas en la base de datos
        
        Returns:
            Lista con nombres de tablas
        """
        result = self.execute_query("SHOW TABLES", fetch_all=True)
        if result:
            return [list(row.values())[0] for row in result]
        return []
    
    def get_table_info(self, table_name: str) -> List[Dict]:
        """
        Obtiene información sobre las columnas de una tabla
        
        Args:
            table_name: Nombre de la tabla
            
        Returns:
            Lista con información de las columnas
        """
        return self.execute_query(f"DESCRIBE {table_name}", fetch_all=True)
    
    def __enter__(self):
        """Soporte para context manager"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra la conexión al salir del contexto"""
        self.disconnect()
    
    def __del__(self):
        """Destructor - asegura que la conexión se cierre"""
        try:
            self.disconnect()
        except:
            pass  # Ignorar errores en el destructor


class YourSQLQueryBuilder:
    """
    Constructor de consultas SQL de forma programática
    """
    
    def __init__(self, connection: YourSQLConnection):
        self.connection = connection
        self.reset()
    
    def reset(self):
        """Reinicia el estado del query builder"""
        self._select = "*"
        self._from = ""
        self._where = []
        self._order_by = []
        self._limit = None
        self._offset = None
        return self
    
    def select(self, *columns: str):
        """Define las columnas a seleccionar"""
        self._select = ", ".join(columns) if columns else "*"
        return self
    
    def from_table(self, table: str):
        """Define la tabla principal"""
        self._from = table
        return self
    
    def where(self, condition: str):
        """Añade una condición WHERE"""
        self._where.append(condition)
        return self
    
    def order_by(self, column: str, direction: str = "ASC"):
        """Añade ORDER BY"""
        self._order_by.append(f"{column} {direction}")
        return self
    
    def limit(self, limit: int):
        """Añade LIMIT"""
        self._limit = limit
        return self
    
    def offset(self, offset: int):
        """Añade OFFSET"""
        self._offset = offset
        return self
    
    def build(self) -> str:
        """Construye la consulta SQL"""
        query = f"SELECT {self._select} FROM {self._from}"
        
        if self._where:
            query += " WHERE " + " AND ".join(self._where)
        
        if self._order_by:
            query += " ORDER BY " + ", ".join(self._order_by)
        
        if self._limit:
            query += f" LIMIT {self._limit}"
        
        if self._offset:
            query += f" OFFSET {self._offset}"
        
        return query
    
    def execute(self):
        """Ejecuta la consulta construida"""
        query = self.build()
        result = self.connection.execute_query(query)
        self.reset()
        return result
