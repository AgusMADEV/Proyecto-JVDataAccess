"""
Configuración de la base de datos
Versión: 1.0.0

Define aquí tus credenciales de base de datos
"""

# Configuración de MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'tu_usuario',       # Cambia esto por tu usuario
    'password': 'tu_contraseña',       # Cambia esto por tu contraseña
    'database': 'jvdataaccess_demo',
    'port': 3306
}

# Configuración alternativa para desarrollo
DB_CONFIG_DEV = {
    'host': 'localhost',
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'database': 'jvdataaccess_demo',
    'port': 3306
}
