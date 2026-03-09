# 🚀 Guía de Migración: v1.0 → v2.0

Esta guía te ayudará a migrar tu código de JVDataAccess 1.0 a la nueva versión 2.0.

## 📊 Resumen de Cambios

### Nuevas Características en v2.0
✅ Pool de conexiones para mejor rendimiento  
✅ Sistema de logging integrado  
✅ Soporte completo para transacciones  
✅ CRUD optimizado con más opciones  
✅ Excepciones personalizadas específicas  
✅ Métodos auxiliares: `contar()`, `existe()`, `insertar_multiple()`  

### Compatibilidad
- ✅ La versión 1.0 sigue funcionando sin cambios
- ✅ Puedes usar ambas versiones en el mismo proyecto
- ✅ Migración gradual recomendada

---

## 🔄 Cambios de Importación

### Python

**Antes (v1.0):**
```python
from src.python.jvdb import JVDB

db = JVDB('localhost', 'user', 'pass', 'db')
```

**Después (v2.0):**
```python
from src.python.jvdb import JVDB2  # o .jvdb2

db = JVDB2('localhost', 'user', 'pass', 'db')
```

### PHP

**Antes (v1.0):**
```php
require_once 'src/php/JVDB/JVDB.php';
use JVDB\JVDB;

$db = new JVDB('localhost', 'user', 'pass', 'db');
```

**Después (v2.0):**
```php
require_once 'src/php/JVDB/JVDB2.php';
use JVDB\JVDB2;

$db = new JVDB2('localhost', 'user', 'pass', 'db');
```

---

## 🔨 Cambios en Métodos

### 1. Seleccionar

**v1.0:**
```python
# Python
usuarios = db.seleccionar('usuarios', formato='list')

# PHP
$usuarios = $db->seleccionar('usuarios', '*', 'array');
```

**v2.0:**
```python
# Python - Más opciones disponibles
usuarios = db.seleccionar(
    'usuarios',
    columnas=['Nombre', 'Email'],  # Opcional
    where={'Activo': 1},           # Opcional
    order_by='Nombre ASC',          # Opcional
    limit=10                         # Opcional
)

# PHP
$usuarios = $db->seleccionar(
    'usuarios',
    ['Nombre', 'Email'],  # Opcional
    ['Activo' => 1],      # Opcional
    'Nombre ASC',          # Opcional
    10                     # Opcional
);
```

### 2. Insertar

**v1.0:**
```python
# Python
resultado = db.insertar('usuarios', datos)
print(f"Filas afectadas: {resultado}")

# PHP
$resultado = $db->insertar('usuarios', $datos);
echo "Filas afectadas: $resultado";
```

**v2.0:**
```python
# Python - Puede retornar el ID insertado
resultado = db.insertar('usuarios', datos, return_id=True)
print(f"ID insertado: {resultado['last_insert_id']}")

# PHP
$resultado = $db->insertar('usuarios', $datos, true);
echo "ID insertado: {$resultado['last_insert_id']}";
```

### 3. Actualizar

**v1.0:**
```python
# Python - Solo por ID
db.actualizar('usuarios', identificador=1, datos={'Nombre': 'Juan'})

# PHP
$db->actualizar('usuarios', 1, ['Nombre' => 'Juan']);
```

**v2.0:**
```python
# Python - Por ID o WHERE personalizado
db.actualizar('usuarios', datos={'Nombre': 'Juan'}, identificador=1)
# O
db.actualizar('usuarios', datos={'Activo': 0}, where={'Email': 'test@test.com'})

# PHP
$db->actualizar('usuarios', ['Nombre' => 'Juan'], 1);
// O
$db->actualizar('usuarios', ['Activo' => 0], null, ['Email' => 'test@test.com']);
```

### 4. Eliminar

**v1.0:**
```python
# Python - Solo por ID
db.eliminar('usuarios', identificador=1)

# PHP
$db->eliminar('usuarios', 1);
```

**v2.0:**
```python
# Python - Por ID o WHERE personalizado
db.eliminar('usuarios', identificador=1)
# O
db.eliminar('usuarios', where={'Activo': 0})

# PHP
$db->eliminar('usuarios', 1);
// O
$db->eliminar('usuarios', null, ['Activo' => 0]);
```

---

## 🆕 Nuevos Métodos en v2.0

### Contar Registros
```python
# Python
total = db.contar('usuarios')
activos = db.contar('usuarios', where={'Activo': 1})

# PHP
$total = $db->contar('usuarios');
$activos = $db->contar('usuarios', ['Activo' => 1]);
```

### Verificar Existencia
```python
# Python
if db.existe('usuarios', {'Email': 'test@test.com'}):
    print("El usuario existe")

# PHP
if ($db->existe('usuarios', ['Email' => 'test@test.com'])) {
    echo "El usuario existe";
}
```

### Inserción Múltiple
```python
# Python
usuarios = [
    {'Nombre': 'Juan', 'Email': 'juan@test.com'},
    {'Nombre': 'Ana', 'Email': 'ana@test.com'}
]
total = db.insertar_multiple('usuarios', usuarios)

# PHP
$usuarios = [
    ['Nombre' => 'Juan', 'Email' => 'juan@test.com'],
    ['Nombre' => 'Ana', 'Email' => 'ana@test.com']
];
$total = $db->insertarMultiple('usuarios', $usuarios);
```

---

## 🔐 Transacciones (Nueva Característica)

### Python
```python
# v2.0 - Context manager automático
with db.transaction():
    db.insertar('usuarios', datos1)
    db.actualizar('pedidos', datos2, identificador=10)
    db.eliminar('temporal', identificador=5)
# Commit automático, rollback si hay error
```

### PHP
```php
// v2.0 - Manejo manual
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

---

## 📝 Manejo de Errores Mejorado

### Python

**v1.0:**
```python
try:
    db.insertar('usuarios', datos)
except Exception as e:
    print(f"Error: {e}")
```

**v2.0:**
```python
from src.python.jvdb.exceptions import ValidationError, QueryError

try:
    db.insertar('usuarios', datos)
except ValidationError as e:
    print(f"Datos inválidos: {e}")
except QueryError as e:
    print(f"Error en consulta: {e}")
```

### PHP

**v1.0:**
```php
try {
    $db->insertar('usuarios', $datos);
} catch (Exception $e) {
    echo "Error: {$e->getMessage()}";
}
```

**v2.0:**
```php
use JVDB\Exceptions\ValidationException;
use JVDB\Exceptions\QueryException;

try {
    $db->insertar('usuarios', $datos);
} catch (ValidationException $e) {
    echo "Datos inválidos: {$e->getMessage()}";
} catch (QueryException $e) {
    echo "Error en consulta: {$e->getMessage()}";
}
```

---

## ⚙️ Configuración del Pool y Logging

### Python
```python
# Opcional - Configurar pool y logging
pool_config = {
    'min_size': 2,
    'max_size': 10,
    'max_lifetime': 3600,
    'timeout': 30
}

log_config = {
    'log_dir': 'logs',
    'console_output': True,
    'file_output': True
}

db = JVDB2(
    'localhost', 'user', 'pass', 'db',
    use_pool=True,
    pool_config=pool_config,
    log_config=log_config
)
```

### PHP
```php
// Opcional
$poolConfig = [
    'min_size' => 2,
    'max_size' => 10
];

$logConfig = [
    'log_dir' => 'logs',
    'console_output' => true
];

$db = new JVDB2(
    'localhost', 'user', 'pass', 'db',
    3306,
    true,  // use_pool
    $poolConfig,
    $logConfig
);
```

---

## 📈 Ejemplo de Migración Completa

### Antes (v1.0)
```python
from src.python.jvdb import JVDB

db = JVDB('localhost', 'user', 'pass', 'db')

# Operaciones básicas
usuarios = db.seleccionar('usuarios')
db.insertar('usuarios', {'Nombre': 'Juan', 'Email': 'juan@test.com'})
db.actualizar('usuarios', 1, {'Activo': 0})
db.eliminar('usuarios', 5)

db.desconectar()
```

### Después (v2.0)
```python
from src.python.jvdb import JVDB2

# Con context manager - cierre automático
with JVDB2('localhost', 'user', 'pass', 'db') as db:
    
    # Operaciones con más opciones
    usuarios = db.seleccionar(
        'usuarios',
        where={'Activo': 1},
        order_by='Nombre ASC',
        limit=10
    )
    
    # Con transacción
    with db.transaction():
        db.insertar('usuarios', {'Nombre': 'Juan', 'Email': 'juan@test.com'})
        db.actualizar('usuarios', datos={'Activo': 0}, identificador=1)
        db.eliminar('usuarios', identificador=5)
    
    # Métodos nuevos
    if db.existe('usuarios', {'Email': 'juan@test.com'}):
        total = db.contar('usuarios', where={'Activo': 1})
        print(f"Usuarios activos: {total}")
# Cierre automático al salir del with
```

---

## ✅ Checklist de Migración

- [ ] Cambiar imports de `JVDB` a `JVDB2`
- [ ] Actualizar llamadas a métodos con nuevas opciones
- [ ] Agregar manejo de excepciones específicas
- [ ] Implementar transacciones donde sea necesario
- [ ] Usar context managers (Python) o try-finally (PHP)
- [ ] Aprovechar nuevos métodos: `contar()`, `existe()`, `insertar_multiple()`
- [ ] Configurar pool y logging según necesidades
- [ ] Probar exhaustivamente antes de pasar a producción

---

## 🔗 Recursos Adicionales

- [Guía completa v2.0](GUIA_V2.md)
- [Ejemplos Python](../examples/python/ejemplo_v2.py)
- [Ejemplos PHP](../examples/php/ejemplo_v2.php)
- [CHANGELOG completo](../CHANGELOG.md)

---

## 💡 Consejos

1. **Migración Gradual**: No necesitas migrar todo de una vez
2. **Pruebas**: Mantén pruebas para ambas versiones durante la transición
3. **Performance**: La v2.0 es más rápida con pool de conexiones
4. **Logs**: Usa el sistema de logging para debugging
5. **Transacciones**: Úsalas para operaciones críticas

---

¿Necesitas ayuda? Consulta la documentación completa en `docs/GUIA_V2.md`
