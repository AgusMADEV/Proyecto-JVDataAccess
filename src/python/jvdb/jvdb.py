"""
JVDB - Clase de Abstracción para Acceso a Base de Datos
Versión: 1.0.0

Proporciona una interfaz simplificada para operaciones comunes
de base de datos utilizando YourSQL como backend.
"""

import json
from typing import Optional, List, Dict, Any, Union

# Import flexible que funciona tanto con imports relativos como absolutos
try:
    from ..yoursql import YourSQLConnection
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from yoursql.yoursql import YourSQLConnection


class JVDB:
    """
    Clase de abstracción para acceso simplificado a base de datos MySQL
    """
    
    def __init__(
        self,
        host: str,
        usuario: str,
        contrasena: str,
        basedatos: str,
        port: int = 3306,
        autoconnect: bool = True
    ):
        """
        Inicializa JVDB con los parámetros de conexión
        
        Args:
            host: Dirección del servidor MySQL
            usuario: Usuario de la base de datos
            contrasena: Contraseña del usuario
            basedatos: Nombre de la base de datos
            port: Puerto de conexión (por defecto 3306)
            autoconnect: Conectar automáticamente (por defecto True)
        """
        self.host = host
        self.usuario = usuario
        self.contrasena = contrasena
        self.basedatos = basedatos
        self.port = port
        
        # Crear conexión usando YourSQL
        self.conexion = YourSQLConnection(
            host=host,
            user=usuario,
            password=contrasena,
            database=basedatos,
            port=port
        )
        
        if autoconnect:
            self.conectar()
    
    def conectar(self) -> bool:
        """
        Establece la conexión con la base de datos
        
        Returns:
            bool: True si la conexión fue exitosa
        """
        resultado = self.conexion.connect()
        if resultado:
            print(f"✅ Conectado a la base de datos '{self.basedatos}'")
        return resultado
    
    def desconectar(self):
        """Cierra la conexión con la base de datos"""
        try:
            if hasattr(self, 'conexion') and self.conexion:
                self.conexion.disconnect()
                print("🔌 Conexión cerrada")
        except Exception as e:
            # Ignorar errores al cerrar
            pass
    
    def esta_conectado(self) -> bool:
        """
        Verifica si hay conexión activa
        
        Returns:
            bool: True si está conectado
        """
        return self.conexion.is_connected()
    
    def seleccionar(
        self,
        tabla: str,
        columnas: str = "*",
        formato: str = "json"
    ) -> Union[str, List[Dict]]:
        """
        Selecciona todos los registros de una tabla
        
        Args:
            tabla: Nombre de la tabla
            columnas: Columnas a seleccionar (por defecto todas)
            formato: 'json' o 'list' (por defecto json)
            
        Returns:
            Datos en el formato especificado
        """
        query = f"SELECT {columnas} FROM {tabla}"
        resultado = self.conexion.execute_query(query, fetch_all=True)
        
        if resultado is None:
            resultado = []
        
        if formato == "json":
            return json.dumps(resultado, ensure_ascii=False, indent=2)
        return resultado
    
    def seleccionar_uno(self, tabla: str, identificador: int) -> Optional[Dict]:
        """
        Selecciona un único registro por su identificador
        
        Args:
            tabla: Nombre de la tabla
            identificador: ID del registro
            
        Returns:
            Diccionario con el registro o None
        """
        query = f"SELECT * FROM {tabla} WHERE Identificador = %s"
        return self.conexion.execute_query(query, params=(identificador,), fetch_one=True)
    
    def buscar(
        self,
        tabla: str,
        columna: str,
        valor: Any,
        formato: str = "json"
    ) -> Union[str, List[Dict]]:
        """
        Busca registros por un criterio específico
        
        Args:
            tabla: Nombre de la tabla
            columna: Columna donde buscar
            valor: Valor a buscar
            formato: 'json' o 'list'
            
        Returns:
            Resultados en el formato especificado
        """
        query = f"SELECT * FROM {tabla} WHERE {columna} LIKE %s"
        like_valor = f"%{valor}%"
        resultado = self.conexion.execute_query(query, params=(like_valor,), fetch_all=True)
        
        if resultado is None:
            resultado = []
        
        if formato == "json":
            return json.dumps(resultado, ensure_ascii=False, indent=2)
        return resultado
    
    def insertar(self, tabla: str, datos: Dict[str, Any]) -> int:
        """
        Inserta un nuevo registro en una tabla
        
        Args:
            tabla: Nombre de la tabla
            datos: Diccionario con columna:valor
            
        Returns:
            Número de filas afectadas
        """
        columnas = ", ".join(datos.keys())
        placeholders = ", ".join(["%s"] * len(datos))
        valores = tuple(datos.values())
        
        query = f"INSERT INTO {tabla} ({columnas}) VALUES ({placeholders})"
        resultado = self.conexion.execute_query(query, params=valores)
        
        if resultado and resultado > 0:
            print(f"✅ Registro insertado en '{tabla}'")
        return resultado if resultado else 0
    
    def actualizar(
        self,
        tabla: str,
        identificador: int,
        datos: Dict[str, Any]
    ) -> int:
        """
        Actualiza un registro existente
        
        Args:
            tabla: Nombre de la tabla
            identificador: ID del registro a actualizar
            datos: Diccionario con columna:valor
            
        Returns:
            Número de filas afectadas
        """
        set_clause = ", ".join([f"{col} = %s" for col in datos.keys()])
        valores = tuple(list(datos.values()) + [identificador])
        
        query = f"UPDATE {tabla} SET {set_clause} WHERE Identificador = %s"
        resultado = self.conexion.execute_query(query, params=valores)
        
        if resultado and resultado > 0:
            print(f"✅ Registro actualizado en '{tabla}'")
        return resultado if resultado else 0
    
    def eliminar(self, tabla: str, identificador: int) -> int:
        """
        Elimina un registro de una tabla
        
        Args:
            tabla: Nombre de la tabla
            identificador: ID del registro a eliminar
            
        Returns:
            Número de filas afectadas
        """
        query = f"DELETE FROM {tabla} WHERE Identificador = %s"
        resultado = self.conexion.execute_query(query, params=(identificador,))
        
        if resultado and resultado > 0:
            print(f"✅ Registro eliminado de '{tabla}'")
        return resultado if resultado else 0
    
    def tablas(self, formato: str = "json") -> Union[str, List[str]]:
        """
        Lista todas las tablas de la base de datos
        
        Args:
            formato: 'json' o 'list'
            
        Returns:
            Lista de tablas en el formato especificado
        """
        resultado = self.conexion.get_tables()
        
        if formato == "json":
            return json.dumps(resultado, ensure_ascii=False, indent=2)
        return resultado
    
    def estructura_tabla(self, tabla: str, formato: str = "json") -> Union[str, List[Dict]]:
        """
        Obtiene la estructura de una tabla
        
        Args:
            tabla: Nombre de la tabla
            formato: 'json' o 'list'
            
        Returns:
            Información de las columnas
        """
        resultado = self.conexion.get_table_info(tabla)
        
        if formato == "json":
            return json.dumps(resultado, ensure_ascii=False, indent=2)
        return resultado
    
    def consulta_personalizada(
        self,
        query: str,
        params: Optional[tuple] = None,
        formato: str = "json"
    ) -> Union[str, List[Dict], int]:
        """
        Ejecuta una consulta SQL personalizada
        
        Args:
            query: Consulta SQL
            params: Parámetros para consultas preparadas
            formato: 'json' o 'list'
            
        Returns:
            Resultados de la consulta
        """
        if query.strip().upper().startswith('SELECT'):
            resultado = self.conexion.execute_query(query, params=params, fetch_all=True)
            if resultado is None:
                resultado = []
            if formato == "json":
                return json.dumps(resultado, ensure_ascii=False, indent=2)
            return resultado
        else:
            # Para INSERT, UPDATE, DELETE
            return self.conexion.execute_query(query, params=params)
    
    def __enter__(self):
        """Soporte para context manager"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra la conexión al salir del contexto"""
        self.desconectar()
    
    def __del__(self):
        """Destructor - asegura que la conexión se cierre"""
        try:
            if hasattr(self, 'conexion'):
                self.desconectar()
        except:
            pass  # Ignorar errores en el destructor
