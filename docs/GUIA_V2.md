# Guía de Uso - JVDataAccess 2.0

**Versión: 2.0.0**

Esta guía detalla las nuevas características de la versión 2.0 de JVDataAccess.

## 📋 Novedades en la Versión 2.0

### ✨ Nuevas Características

1. **Sistema de Logging Integrado**
   - Registro automático de todas las operaciones
   - Logs en archivo y consola
   - Niveles de logging configurables

2. **Pool de Conexiones**
   - Gestión eficiente de múltiples conexiones
   - Mejora significativa del rendimiento
   - Configuración flexible (min/max conexiones, timeout, etc.)

3. **CRUD Completo Optimizado**
   - Métodos mejorados con más opciones
   - Soporte para WHERE, ORDER BY, LIMIT, OFFSET
   - Inserción múltiple optimizada
   - Métodos auxiliares: `contar()`, `existe()`

4. **Sistema de Transacciones**
   - Context managers para transacciones seguras
   - Rollback automático en caso de error
   - Soporte para operaciones complejas

5. **Manejo Robusto de Errores**
   - Excepciones personalizadas específicas
   - Mejor rastreo de errores
   - Mensajes de error más descriptivos

---

## 🚀 Instalación y Configuración

### Python

```python
from src.python.jvdb.jvdb2 import JVDB2

# Configuración del pool
pool_config = {
    'min_size': 2,        # Conexiones mínimas
    'max_size': 10,       # Conexiones máximas
    'max_lifetime': 3600, # Tiempo de vida (segundos)
    'timeout': 30         # Timeout para obtener conexión
}

# Configuración del logger
log_config = {
    'log_dir': 'logs',
    'log_level': logging.INFO,
    'console_output': True,
    'file_output': True
}

# Crear instancia
db = JVDB2(
    'localhost',
    'usuario',
    'password',
    'database',
    use_pool=True,
    pool_config=pool_config,
    log_config=log_config
)
```

### PHP

```php
use JVDB\JVDB2;

// Configuración del pool
$poolConfig = [
    'min_size' => 2,
    'max_size' => 10,
    'max_lifetime' => 3600,
    'timeout' => 30
];

// Configuración del logger
$logConfig = [
    'log_dir' => 'logs',
    'console_output' => true,
    'file_output' => true
];

// Crear instancia
$db = new JVDB2(
    'localhost',
    'usuario',
    'password',
    'database',
    3306,
    true,  // use_pool
    $poolConfig,
    $logConfig
);
```

---

## 📚 Guía de Uso

### 1. SELECT Avanzado

**Python:**
```python
# SELECT simple
usuarios = db.seleccionar('usuarios')

# SELECT con opciones
usuarios = db.seleccionar(
    tabla='usuarios',
    columnas=['Nombre', 'Email', 'Edad'],
    where={'Activo': 1},
    order_by='Nombre ASC',
    limit=10,
    offset=0
)

# SELECT uno
usuario = db.seleccionar_uno(
    'usuarios',
    identificador=1
)

# O con WHERE personalizado
usuario = db.seleccionar_uno(
    'usuarios',
    where={'Email': 'ejemplo@email.com'}
)
```

**PHP:**
```php
// SELECT simple
$usuarios = $db->seleccionar('usuarios');

// SELECT con opciones
$usuarios = $db->seleccionar(
    'usuarios',
    ['Nombre', 'Email', 'Edad'],
    ['Activo' => 1],
    'Nombre ASC',
    10,
    0
);

// SELECT uno
$usuario = $db->seleccionarUno('usuarios', 1);

// O con WHERE personalizado
$usuario = $db->seleccionarUno(
    'usuarios',
    null,
    ['Email' => 'ejemplo@email.com']
);
```

### 2. INSERT Mejorado

**Python:**
```python
# INSERT simple
filas = db.insertar('usuarios', {
    'Nombre': 'Juan',
    'Email': 'juan@example.com',
    'Edad': 30
})

# INSERT con ID retornado
resultado = db.insertar('usuarios', datos, return_id=True)
print(f"ID insertado: {resultado['last_insert_id']}")

# INSERT múltiple (con transacción automática)
usuarios = [
    {'Nombre': 'Ana', 'Email': 'ana@example.com'},
    {'Nombre': 'Luis', 'Email': 'luis@example.com'},
    {'Nombre': 'María', 'Email': 'maria@example.com'}
]
total = db.insertar_multiple('usuarios', usuarios)
```

**PHP:**
```php
// INSERT simple
$filas = $db->insertar('usuarios', [
    'Nombre' => 'Juan',
    'Email' => 'juan@example.com',
    'Edad' => 30
]);

// INSERT con ID retornado
$resultado = $db->insertar('usuarios', $datos, true);
echo "ID insertado: {$resultado['last_insert_id']}";

// INSERT múltiple
$usuarios = [
    ['Nombre' => 'Ana', 'Email' => 'ana@example.com'],
    ['Nombre' => 'Luis', 'Email' => 'luis@example.com'],
    ['Nombre' => 'María', 'Email' => 'maria@example.com']
];
$total = $db->insertarMultiple('usuarios', $usuarios);
```

### 3. UPDATE Mejorado

**Python:**
```python
# UPDATE por ID
db.actualizar(
    'usuarios',
    datos={'Nombre': 'Juan Carlos'},
    identificador=1
)

# UPDATE con WHERE personalizado
db.actualizar(
    'usuarios',
    datos={'Activo': 0},
    where={'Email': 'ejemplo@email.com'}
)
```

**PHP:**
```php
// UPDATE por ID
$db->actualizar(
    'usuarios',
    ['Nombre' => 'Juan Carlos'],
    1
);

// UPDATE con WHERE personalizado
$db->actualizar(
    'usuarios',
    ['Activo' => 0],
    null,
    ['Email' => 'ejemplo@email.com']
);
```

### 4. DELETE Mejorado

**Python:**
```python
# DELETE por ID
db.eliminar('usuarios', identificador=1)

# DELETE con WHERE
db.eliminar('usuarios', where={'Activo': 0})
```

**PHP:**
```php
// DELETE por ID
$db->eliminar('usuarios', 1);

// DELETE con WHERE
$db->eliminar('usuarios', null, ['Activo' => 0]);
```

### 5. Métodos Auxiliares

**Python:**
```python
# Contar registros
total = db.contar('usuarios')
activos = db.contar('usuarios', where={'Activo': 1})

# Verificar existencia
existe = db.existe('usuarios', {'Email': 'test@example.com'})
if existe:
    print("El usuario ya existe")
```

**PHP:**
```php
// Contar registros
$total = $db->contar('usuarios');
$activos = $db->contar('usuarios', ['Activo' => 1]);

// Verificar existencia
$existe = $db->existe('usuarios', ['Email' => 'test@example.com']);
if ($existe) {
    echo "El usuario ya existe";
}
```

### 6. Transacciones

**Python:**
```python
# Usando context manager
with db.transaction():
    db.insertar('usuarios', datos1)
    db.actualizar('pedidos', datos2, identificador=10)
    db.eliminar('temporal', identificador=5)
# Commit automático al salir, rollback si hay error
```

**PHP:**
```php
// Manejo manual de transacciones
$db->beginTransaction();

try {
    $db->insertar('usuarios', $datos1);
    $db->actualizar('pedidos', $datos2, 10);
    $db->eliminar('temporal', 5);
    
    $db->commit();
} catch (Exception $e) {
    $db->rollback();
    throw $e;
}
```

### 7. Consultas Personalizadas

**Python:**
```python
# SELECT personalizado
resultado = db.consulta_personalizada(
    "SELECT * FROM usuarios WHERE Edad > %s AND Activo = %s",
    params=(25, 1),
    fetch="all"
)

# INSERT/UPDATE/DELETE personalizado
filas = db.consulta_personalizada(
    "UPDATE usuarios SET Activo = %s WHERE Edad < %s",
    params=(0, 18),
    fetch="none"
)
```

**PHP:**
```php
// SELECT personalizado
$resultado = $db->consultaPersonalizada(
    "SELECT * FROM usuarios WHERE Edad > ? AND Activo = ?",
    [25, 1]
);

// INSERT/UPDATE/DELETE personalizado
$filas = $db->consultaPersonalizada(
    "UPDATE usuarios SET Activo = ? WHERE Edad < ?",
    [0, 18]
);
```

### 8. Estadísticas del Pool

**Python:**
```python
stats = db.get_pool_stats()
print(f"Conexiones totales: {stats['total_connections']}")
print(f"En uso: {stats['in_use']}")
print(f"Disponibles: {stats['available']}")
```

**PHP:**
```php
$stats = $db->getPoolStats();
echo "Conexiones totales: {$stats['total_connections']}\n";
echo "En uso: {$stats['in_use']}\n";
echo "Disponibles: {$stats['available']}\n";
```

### 9. Context Manager / Try-Finally

**Python:**
```python
# Usando with (recomendado)
with JVDB2(...) as db:
    usuarios = db.seleccionar('usuarios')
    # Cierre automático al salir
```

**PHP:**
```php
// Usando try-finally
$db = new JVDB2(...);
try {
    $usuarios = $db->seleccionar('usuarios');
} finally {
    $db->cerrar();
}
```

---

## 🔒 Manejo de Errores

### Excepciones Disponibles

**Python:**
- `JVDBException` - Excepción base
- `ConnectionError` - Error de conexión
- `QueryError` - Error en consulta SQL
- `TransactionError` - Error en transacción
- `PoolExhaustedError` - Pool agotado
- `ValidationError` - Error de validación
- `ConfigurationError` - Error de configuración

**PHP:**
- `JVDBException` - Excepción base
- `ConnectionException` - Error de conexión
- `QueryException` - Error en consulta SQL
- `TransactionException` - Error en transacción
- `PoolExhaustedException` - Pool agotado
- `ValidationException` - Error de validación
- `ConfigurationException` - Error de configuración

### Ejemplo de Manejo

**Python:**
```python
from src.python.jvdb.exceptions import *

try:
    db.insertar('usuarios', datos)
except ValidationError as e:
    print(f"Datos inválidos: {e}")
except QueryError as e:
    print(f"Error en la consulta: {e}")
except ConnectionError as e:
    print(f"Error de conexión: {e}")
```

**PHP:**
```php
use JVDB\Exceptions\*;

try {
    $db->insertar('usuarios', $datos);
} catch (ValidationException $e) {
    echo "Datos inválidos: {$e->getMessage()}";
} catch (QueryException $e) {
    echo "Error en la consulta: {$e->getMessage()}";
} catch (ConnectionException $e) {
    echo "Error de conexión: {$e->getMessage()}";
}
```

---

## 📊 Sistema de Logging

Los logs se guardan automáticamente en el directorio especificado (por defecto `logs/`).

### Formato de Logs

```
2024-03-09 10:30:45 - JVDB2 - INFO - Conexión exitosa a localhost/mi_base_datos
2024-03-09 10:30:46 - JVDB2 - INFO - SQL: SELECT * FROM usuarios WHERE Activo = %s | Params: (1,)
2024-03-09 10:30:46 - JVDB2 - INFO - 25 registros seleccionados de 'usuarios'
2024-03-09 10:30:47 - JVDB2 - INFO - Transacción: BEGIN
2024-03-09 10:30:48 - JVDB2 - INFO - Transacción: COMMIT
```

### Configurar Nivel de Log

**Python:**
```python
import logging

log_config = {
    'log_level': logging.DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
}

db = JVDB2(..., log_config=log_config)
```

**PHP:**
```php
use JVDB\JVLogger;

$logConfig = [
    'log_level' => JVLogger::DEBUG  // DEBUG, INFO, WARNING, ERROR, CRITICAL
];

$db = new JVDB2(..., $logConfig);
```

---

## ⚡ Optimización del Rendimiento

### Mejores Prácticas

1. **Usar Pool de Conexiones**
   ```python
   db = JVDB2(..., use_pool=True)  # Recomendado para aplicaciones con múltiples consultas
   ```

2. **Inserción Múltiple**
   ```python
   # ✅ Bueno - Una transacción para todos
   db.insertar_multiple('usuarios', lista_usuarios)
   
   # ❌ Malo - Múltiples transacciones
   for usuario in lista_usuarios:
       db.insertar('usuarios', usuario)
   ```

3. **Usar Transacciones para Operaciones Relacionadas**
   ```python
   with db.transaction():
       pedido_id = db.insertar('pedidos', pedido)
       for item in items:
           db.insertar('items_pedido', item)
   ```

4. **Selecciones con LIMIT**
   ```python
   # ✅ Bueno - Limita resultados
   usuarios = db.seleccionar('usuarios', limit=100)
   
   # ❌ Malo - Carga todo en memoria
   usuarios = db.seleccionar('usuarios')
   ```

---

## 🔄 Migración desde v1.0

### Cambios Principales

| v1.0 | v2.0 |
|------|------|
| `JVDB` | `JVDB2` |
| Sin pool | Pool de conexiones integrado |
| Sin logging | Sistema de logging automático |
| Sin transacciones | Context manager para transacciones |
| WHERE limitado | WHERE con diccionarios |
| Sin métodos auxiliares | `contar()`, `existe()`, etc. |

### Ejemplo de Migración

**Antes (v1.0):**
```python
from src.python.jvdb import JVDB

db = JVDB('localhost', 'user', 'pass', 'db')
usuarios = db.seleccionar('usuarios', formato='list')
db.desconectar()
```

**Después (v2.0):**
```python
from src.python.jvdb.jvdb2 import JVDB2

with JVDB2('localhost', 'user', 'pass', 'db') as db:
    usuarios = db.seleccionar('usuarios')  # formato 'list' por defecto
```

---

## 📦 Ejemplos Completos

Consulta los ejemplos completos en:
- Python: `examples/python/ejemplo_v2.py`
- PHP: `examples/php/ejemplo_v2.php`

Para ejecutarlos:

```bash
# Python
python examples/python/ejemplo_v2.py

# PHP
php examples/php/ejemplo_v2.php
```

---

## 🐛 Solución de Problemas

### Pool Agotado

```
PoolExhaustedError: No se pudo obtener conexión en 30 segundos
```

**Solución:**
- Aumentar `max_size` del pool
- Aumentar `timeout`
- Verificar que las conexiones se liberan correctamente

### Errores de Transacción

```
TransactionError: No hay transacción activa
```

**Solución:**
- Asegurarse de llamar `beginTransaction()` antes de `commit()`
- Usar context manager en Python

### Logs Muy Grandes

**Solución:**
- Cambiar nivel de log a `WARNING` o `ERROR`
- Implementar rotación de logs
- Desactivar `file_output` si no es necesario

---

## 📞 Soporte

Para más información, consulta:
- [README.md](../README.md)
- [ROADMAP.md](ROADMAP.md)
- [CHANGELOG.md](../CHANGELOG.md)
