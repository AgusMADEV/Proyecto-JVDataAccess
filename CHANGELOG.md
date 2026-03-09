# Changelog - JVDataAccess

Todos los cambios importantes del proyecto se documentarán en este archivo.

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
