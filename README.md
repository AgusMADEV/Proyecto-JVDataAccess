# JVDataAccess - Sistema Modular de Acceso a Datos

**Versión actual: 1.0.0**

## 📋 Descripción

JVDataAccess es un sistema completo y modular para el acceso a datos en Python y PHP. Incluye:

- **YourSQL**: Conector MySQL personalizado con mejoras sobre drivers nativos
- **JVDB**: Clase de abstracción para bases de datos (Python y PHP)
- **JVORM**: ORM (Object-Relational Mapping) para persistencia de objetos
- **Arquitectura modular**: Diseñado como librería reutilizable

## 🚀 Versiones del Proyecto

### Versión 1.0 (Actual)
- ✅ Conector básico YourSQL
- ✅ Clase JVDB con operaciones fundamentales
- ✅ Soporte para Python y PHP
- ✅ Sistema de gestión de conexiones

### Versión 2.0 (Planificada)
- CRUD completo optimizado
- Prepared statements avanzados
- Sistema de logging
- Manejo robusto de errores

### Versión 3.0 (Planificada)
- ORM completo (JVORM)
- Mapeo objeto-relacional
- Anotaciones y decoradores
- Relaciones entre entidades

### Versión 4.0 (Planificada)
- Sistema de transacciones avanzado
- Pool de conexiones
- Caché de consultas
- Sistema de migraciones

## 📂 Estructura del Proyecto

```
JVDataAccess/
├── src/
│   ├── python/
│   │   ├── yoursql/          # Conector MySQL personalizado
│   │   ├── jvdb/             # Abstracción de base de datos
│   │   └── jvorm/            # ORM
│   └── php/
│       ├── YourSQL/
│       ├── JVDB/
│       └── JVORM/
├── examples/
│   ├── python/               # Ejemplos en Python
│   └── php/                  # Ejemplos en PHP
├── tests/
│   ├── python/               # Tests unitarios Python
│   └── php/                  # Tests unitarios PHP
├── docs/                     # Documentación completa
└── database/                 # Scripts SQL de ejemplo
```

## 💻 Instalación

### Python
```bash
# Instalar dependencias
pip install -r requirements.txt

# Importar la librería
from src.python.jvdb import JVDB
```

### PHP
```php
<?php
require_once 'src/php/JVDB/JVDB.php';
use JVDB\JVDB;
?>
```

## 📖 Uso Básico

### Python
```python
from src.python.jvdb import JVDB

# Crear conexión
db = JVDB('localhost', 'usuario', 'password', 'database')

# Consultar datos
datos = db.seleccionar('usuarios')
print(datos)
```

### PHP
```php
<?php
$db = new JVDB('localhost', 'usuario', 'password', 'database');
$datos = $db->seleccionar('usuarios');
echo $datos;
?>
```

## 🎯 Características Principales

- **Abstracción de bajo nivel**: YourSQL proporciona control total
- **API simple**: JVDB ofrece métodos intuitivos
- **Multiplataforma**: Funciona en Python y PHP
- **ORM integrado**: JVORM para desarrollo orientado a objetos (v3.0)
- **Seguridad**: Protección contra SQL injection
- **Rendimiento**: Optimizado para operaciones intensivas

## 👨‍💻 Autor

Proyecto desarrollado como actividad final de la asignatura de Acceso a Datos - DAM 2

## 📄 Licencia

