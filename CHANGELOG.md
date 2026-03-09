# Changelog - JVDataAccess

Todos los cambios importantes del proyecto se documentarán en este archivo.

## [2.0.0] - 2026-03-09

### ✨ Características Nuevas

- **Menú Interactivo v2.0**: Sistema de menú interactivo para explorar funcionalidades
  - Interfaz de consola intuitiva en Python y PHP
  - 10 ejemplos prácticos listos para usar
  - Operaciones CRUD completas con guías paso a paso
  - Demostración de transacciones con rollback
  - Visualización en tiempo real de estadísticas del pool
  - Gestión de errores educativa
  - Visualizador de logs integrado
  - Pruebas de inserción múltiple (batch)
  - Scripts auxiliares: `crear_tabla_usuarios.py` y `crear_tabla_usuarios.php`

- **JVDB2**: Nueva versión mejorada de la clase de abstracción
  - Pool de conexiones reutilizables para mejor rendimiento
  - Sistema de logging integrado con múltiples niveles
  - Soporte completo para transacciones con rollback automático
  - CRUD optimizado con opciones avanzadas (WHERE, ORDER BY, LIMIT, OFFSET)
  - Métodos auxiliares: `contar()`, `existe()`, `insertar_multiple()`
  - Manejo robusto de errores con excepciones personalizadas
  - Context managers para gestión automática de recursos

- **JVConnectionPool**: Sistema de pool de conexiones
  - Configuración flexible (min/max conexiones, timeout, lifetime)
  - Gestión automática del ciclo de vida de conexiones
  - Estadísticas en tiempo real del pool
  - Validación automática de conexiones
  - Soporte para Python y PHP

- **JVLogger**: Sistema de logging profesional
  - Logs en archivo y consola
  - Niveles configurables (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - Formato estructurado con timestamps
  - Registro específico de consultas SQL
  - Tracking de transacciones y conexiones

- **Sistema de Excepciones**: Manejo de errores robusto
  - `ConnectionError/ConnectionException`: Errores de conexión
  - `QueryError/QueryException`: Errores en consultas SQL
  - `TransactionError/TransactionException`: Errores en transacciones
  - `PoolExhaustedError/PoolExhaustedException`: Pool agotado
  - `ValidationError/ValidationException`: Errores de validación
  - `ConfigurationError/ConfigurationException`: Errores de configuración

### 🚀 Mejoras

- **CRUD Optimizado**:
  - SELECT con WHERE dinámico, ORDER BY, LIMIT y OFFSET
  - INSERT con opción de retornar último ID insertado
  - UPDATE y DELETE con WHERE flexible
  - Inserción múltiple optimizada con transacciones automáticas
  - Prepared statements mejorados en todas las operaciones

- **Transacciones**:
  - Context manager en Python para transacciones seguras
  - Rollback automático en caso de error
  - Logging de todas las operaciones transaccionales
  - Soporte para operaciones complejas multi-tabla

- **Rendimiento**:
  - Pool de conexiones reduce overhead de conexiones repetidas
  - Reutilización eficiente de conexiones
  - Gestión optimizada de recursos
  - Validación automática de conexiones caducadas

### 📁 Nuevos Archivos

**Python:**
- `src/python/jvdb/jvdb2.py` - Clase JVDB versión 2.0
- `src/python/jvdb/connection_pool.py` - Pool de conexiones
- `src/python/jvdb/logger.py` - Sistema de logging
- `src/python/jvdb/exceptions.py` - Excepciones personalizadas
- `examples/python/ejemplo_v2.py` - Ejemplos de uso v2.0

**PHP:**
- `src/php/JVDB/JVDB2.php` - Clase JVDB versión 2.0
- `src/php/JVDB/JVConnectionPool.php` - Pool de conexiones
- `src/php/JVDB/JVLogger.php` - Sistema de logging
- `src/php/JVDB/JVExceptions.php` - Excepciones personalizadas
- `examples/php/ejemplo_v2.php` - Ejemplos de uso v2.0

**Documentación:**
- `docs/GUIA_V2.md` - Guía completa de uso de la versión 2.0

### 📚 Documentación

- Guía detallada de uso de todas las nuevas características
- Ejemplos completos de CRUD, transacciones, logging y pool
- Guía de migración desde v1.0 a v2.0
- Mejores prácticas de rendimiento
- Solución de problemas comunes

### 🔄 Cambios de API

- La versión 1.0 (JVDB) sigue disponible y funcional
- La versión 2.0 (JVDB2) es la recomendada para nuevos proyectos
- Ambas versiones pueden coexistir en el mismo proyecto
- Migración gradual recomendada para proyectos existentes

### 🎯 Próxima Versión

**Versión 3.0** (Planificada):
- ORM completo (JVORM)
- Mapeo objeto-relacional
- Anotaciones y decoradores
- Relaciones entre entidades (one-to-many, many-to-many)
- Lazy loading
- Query builder fluido

---

## [1.0.0] - 2026-03-06

### ✨ Características Nuevas
- **YourSQL**: Conector MySQL personalizado
  - Soporte para Python y PHP
  - Conexiones persistentes y manejo automático
  - Query Builder para construcción programática de consultas
  - Prepared statements para prevención de SQL injection
  - Context manager support (Python)

- **JVDB**: Clase de abstracción para base de datos
  - API simplificada para operaciones CRUD
  - Métodos intuitivos: `seleccionar()`, `insertar()`, `actualizar()`, `eliminar()`
  - Soporte para consultas personalizadas
  - Formato de salida configurable (JSON/Array/List)
  - Múltiples métodos de búsqueda y filtrado

- **Infraestructura**:
  - Scripts SQL de inicialización
  - Ejemplos completos en Python y PHP
  - Configuración modular
  - Documentación detallada

### 📁 Estructura del Proyecto
```
JVDataAccess/
├── src/
│   ├── python/
│   │   ├── yoursql/
│   │   └── jvdb/
│   └── php/
│       ├── YourSQL/
│       └── JVDB/
├── examples/
├── database/
└── docs/
```

### 🎯 Próximas Versiones

**Versión 2.0** (Planificada):
- Sistema de logging avanzado
- Pool de conexiones
- Caché de consultas
- Mejoras de rendimiento

**Versión 3.0** (Planificada):
- JVORM: ORM completo
- Mapeo objeto-relacional
- Decoradores y anotaciones
- Relaciones entre entidades (One-to-Many, Many-to-Many)

**Versión 4.0** (Planificada):
- Sistema de migraciones
- Versionado de esquemas
- Query optimization
- Métricas y monitorización
