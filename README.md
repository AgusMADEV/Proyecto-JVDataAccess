# JVDataAccess - Sistema Modular de Acceso a Datos

**Versión actual: 2.0.0**

## 📋 Descripción

JVDataAccess es un sistema completo y modular para el acceso a datos en Python y PHP. Incluye:

- **YourSQL**: Conector MySQL personalizado con mejoras sobre drivers nativos
- **JVDB**: Clase de abstracción para bases de datos (Python y PHP)
- **JVORM**: ORM (Object-Relational Mapping) para persistencia de objetos
- **Arquitectura modular**: Diseñado como librería reutilizable

## ⚡ Inicio Rápido

¿Quieres probar JVDataAccess v2.0 de inmediato? Usa el menú interactivo:

```bash
# 1. Crear la base de datos y tablas
python crear_tabla_usuarios.py

# 2. Ejecutar el menú interactivo
python examples/python/menu_interactivo_v2.py
# O en PHP
php examples/php/menu_interactivo_v2.php
```

El menú interactivo te permite explorar todas las funcionalidades de la versión 2.0 sin escribir código.

## 🚀 Versiones del Proyecto

### Versión 1.0
- ✅ Conector básico YourSQL
- ✅ Clase JVDB con operaciones fundamentales
- ✅ Soporte para Python y PHP
- ✅ Sistema de gestión de conexiones

### Versión 2.0 (Actual)
- ✅ CRUD completo optimizado
- ✅ Pool de conexiones
- ✅ Sistema de logging integrado
- ✅ Manejo robusto de errores con excepciones personalizadas
- ✅ Soporte para transacciones
- ✅ Prepared statements avanzados
- ✅ Métodos auxiliares (contar, existe, insertar_multiple)

### Versión 3.0 (Planificada)
- ORM completo (JVORM)
- Mapeo objeto-relacional
- Anotaciones y decoradores
- Relaciones entre entidades (savepoints)
- Caché de consultas
- Sistema de migraciones
- Query builder avanzadoes avanzado
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

# Importar la librería (Versión 2.0)
from src.python.jvdb.jvdb2 import JVDB2

# O usar la versión 1.0 (legacy)
from src.python.jvdb import JVDB
```

### PHP
```php
<?php
// Versión 2.0
require_once 'src/php/JVDB/JVDB2.php';
use JVDB\JVDB2;

// O versión 1.0 (legacy)
require_once 'src/php/JVDB/JVDB.php';
use JVDB\JVDB;
?>
```

## 📖 Uso Básico

### Python (v2.0)
```python
from src.python.jvdb.jvdb2 import JVDB2

# Crear conexión con pool
with JVDB2('localhost', 'usuario', 'password', 'database') as db:
    # Consultar con opciones avanzadas
    usuarios = db.seleccionar(
        'usuarios',
        where={'Activo': 1},
        order_by='Nombre ASC',
        limit=10
    )
    
    # Insertar con transacción
    with db.transaction():
        db.insertar('usuarios', {'Nombre': 'Juan', 'Email': 'juan@example.com'})
        db.actualizar('estadisticas', {'total': 100}, identificador=1)
```Pool de Conexiones**: Gestión eficiente de múltiples conexiones (v2.0)
- **Sistema de Logging**: Registro automático de todas las operaciones (v2.0)
- **Transacciones**: Soporte completo con rollback automático (v2.0)
- **CRUD Optimizado**: Métodos avanzados con WHERE, ORDER BY, LIMIT (v2.0)
- **Manejo de Errores**: Excepciones personalizadas específicas (v2.0)
- **

### PHP (v2.0)
```php
<?php
use JVDB\JVDB2;

$db = new JVDB2('localhost', 'usuario', 'password', 'database');

// Consultar con opciones avanzadas
$usuarios = $db->seleccionar(
    'usuarios',
    ['Nombre', 'Email'],
    ['Activo' => 1],
    'Nombre ASC',
    10
);

// Insertar con transacción
$db->beginTransaction();
try {
    $db->insertar('usuarios', ['Nombre' => 'Juan', 'Email' => 'juan@example.com']);
    $db->actualizar('estadisticas', ['total' => 100], 1);
    $db->commit();
} catch (Exception $e) {
    $db->rollback();
}

$db->cerrar();
?>
```

## � Menú Interactivo v2.0

¡Ahora puedes probar todas las funcionalidades de JVDataAccess v2.0 con un menú interactivo!

### Python
```bash
python examples/python/menu_interactivo_v2.py
```

### PHP
```bash
php examples/php/menu_interactivo_v2.php
```

**Características del menú:**
- ✅ 10 ejemplos prácticos de uso
- ✅ Interfaz intuitiva de consola
- ✅ Operaciones CRUD completas
- ✅ Demostración de transacciones
- ✅ Estadísticas del pool de conexiones
- ✅ Gestión de errores en tiempo real
- ✅ Visualización de logs
- ✅ Inserción múltiple (batch)
- ✅ Búsquedas avanzadas con filtros

**Ejemplos disponibles:**
1. Listado básico de registros
2. Búsquedas avanzadas con filtros
3. Inserción de un registro
4. Inserción múltiple (batch)
5. Actualización de registros
6. Eliminación de registros
7. Demostración de transacciones
8. Estadísticas y agregaciones
9. Configuración personalizada del pool (solo Python)
10. Manejo de errores y excepciones

## �🎯 Características Principales

- **Abstracción de bajo nivel**: YourSQL proporciona control total
- **API simple**: JVDB ofrece métodos intuitivos
- **Multiplataforma**: Funciona en Python y PHP
- **ORM integrado**: JVORM para desarrollo orientado a objetos (v3.0)
- **Seguridad**: Protección contra SQL injection
- **Rendimiento**: Optimizado para operaciones intensivas

## 👨‍💻 Autor

Proyecto desarrollado como actividad final de la asignatura de Acceso a Datos - DAM 2

## 📄 Licencia

