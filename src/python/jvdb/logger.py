"""
JVLogger - Sistema de Logging para JVDataAccess
Versión: 2.0.0

Sistema de registro de eventos y operaciones de base de datos
"""

import logging
import os
from datetime import datetime
from typing import Optional
from pathlib import Path


class JVLogger:
    """
    Sistema de logging personalizado para JVDataAccess
    """
    
    _instances = {}
    
    def __init__(
        self,
        name: str = "JVDB",
        log_dir: str = "logs",
        log_level: int = logging.INFO,
        console_output: bool = True,
        file_output: bool = True
    ):
        """
        Inicializa el sistema de logging
        
        Args:
            name: Nombre del logger
            log_dir: Directorio donde guardar los logs
            log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            console_output: Mostrar logs en consola
            file_output: Guardar logs en archivo
        """
        self.name = name
        self.log_dir = log_dir
        self.log_level = log_level
        
        # Crear directorio de logs si no existe
        if file_output:
            Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        # Configurar logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.logger.handlers.clear()  # Limpiar handlers existentes
        
        # Formato de los mensajes
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para archivo
        if file_output:
            fecha = datetime.now().strftime('%Y-%m-%d')
            log_file = os.path.join(log_dir, f'{name}_{fecha}.log')
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        
        # Handler para consola
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
    
    @classmethod
    def get_instance(cls, name: str = "JVDB", **kwargs) -> 'JVLogger':
        """
        Obtiene una instancia singleton del logger
        
        Args:
            name: Nombre del logger
            **kwargs: Argumentos adicionales para el constructor
            
        Returns:
            Instancia del logger
        """
        if name not in cls._instances:
            cls._instances[name] = cls(name, **kwargs)
        return cls._instances[name]
    
    def debug(self, mensaje: str):
        """Registra un mensaje de debug"""
        self.logger.debug(mensaje)
    
    def info(self, mensaje: str):
        """Registra un mensaje informativo"""
        self.logger.info(mensaje)
    
    def warning(self, mensaje: str):
        """Registra una advertencia"""
        self.logger.warning(mensaje)
    
    def error(self, mensaje: str, exc_info: bool = False):
        """Registra un error"""
        self.logger.error(mensaje, exc_info=exc_info)
    
    def critical(self, mensaje: str, exc_info: bool = False):
        """Registra un error crítico"""
        self.logger.critical(mensaje, exc_info=exc_info)
    
    def query(self, query: str, params: Optional[tuple] = None):
        """
        Registra una consulta SQL
        
        Args:
            query: Consulta SQL
            params: Parámetros de la consulta
        """
        if params:
            self.logger.info(f"SQL: {query} | Params: {params}")
        else:
            self.logger.info(f"SQL: {query}")
    
    def connection(self, host: str, database: str, success: bool = True):
        """
        Registra un intento de conexión
        
        Args:
            host: Host de la base de datos
            database: Nombre de la base de datos
            success: Si la conexión fue exitosa
        """
        if success:
            self.logger.info(f"Conexión exitosa a {host}/{database}")
        else:
            self.logger.error(f"Error al conectar a {host}/{database}")
    
    def transaction(self, action: str):
        """
        Registra una operación de transacción
        
        Args:
            action: Acción realizada (BEGIN, COMMIT, ROLLBACK)
        """
        self.logger.info(f"Transacción: {action}")
    
    def set_level(self, level: int):
        """
        Cambia el nivel de logging
        
        Args:
            level: Nuevo nivel (logging.DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)
