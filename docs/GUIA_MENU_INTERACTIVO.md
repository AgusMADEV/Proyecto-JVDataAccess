# 🎮 Guía del Menú Interactivo v2.0

El menú interactivo de JVDataAccess v2.0 es la forma más rápida de explorar todas las funcionalidades del sistema sin necesidad de escribir código.

## 🚀 Inicio Rápido

### Requisitos Previos

1. **Base de datos configurada**
   ```bash
   # Python
   python crear_tabla_usuarios.py
   
   # PHP
   php crear_tabla_usuarios.php
   ```

2. **Configuración actualizada**
   - Edita `config.py` (Python) o `config.php` (PHP)
   - Configura los datos de conexión a tu base de datos MySQL

### Ejecutar el Menú

```bash
# Python
python examples/python/menu_interactivo_v2.py

# PHP
php examples/php/menu_interactivo_v2.php
```

## 📚 Opciones del Menú

### EJEMPLOS CRUD BÁSICOS

#### 1. Listado básico de registros
Muestra todos los usuarios y productos de la base de datos con estado del pool de conexiones.

**Qué aprenderás:**
- Consultas SELECT básicas
- Visualización de estadísticas del pool
- Uso del método `seleccionar()`
- Uso del método `contar()`

#### 2. Búsquedas avanzadas con filtros
Realiza búsquedas con condiciones WHERE, ORDER BY y consultas personalizadas.

**Qué aprenderás:**
- Filtrado con diccionario WHERE
- Ordenamiento con ORDER BY
- Consultas SQL personalizadas
- Verificación de existencia con `existe()`

#### 3. Inserción de un registro
Inserta un nuevo usuario validando que el email no esté duplicado.

**Qué aprenderás:**
- Inserción con validación previa
- Uso de `insertar()` con `return_id=True`
- Verificación con `existe()`
- Manejo de IDs autogenerados

#### 4. Inserción múltiple (batch)
Inserta varios registros en una sola transacción optimizada.

**Qué aprenderás:**
- Inserción masiva eficiente
- Transacciones automáticas
- Método `insertar_multiple()`
- Rollback automático en caso de error

#### 5. Actualización de registros
Modifica registros existentes (estado, edad, email).

**Qué aprenderás:**
- Actualización con WHERE
- Validación de duplicados antes de actualizar
- Método `actualizar()`
- Contador de filas afectadas

#### 6. Eliminación de registros
Elimina usuarios de prueba de forma segura.

**Qué aprenderás:**
- Eliminación con confirmación
- Búsquedas con LIKE en SQL
- Método `eliminar()`
- Verificación post-eliminación

### ⚙️ FUNCIONALIDADES AVANZADAS

#### 7. Demostración de transacciones
Muestra cómo funcionan las transacciones y el rollback automático.

**Qué aprenderás:**
- Inicio de transacciones
- Commit de cambios
- Rollback automático en errores
- Context manager (Python) / Manejo manual (PHP)

#### 8. Estadísticas y agregaciones
Visualiza estadísticas del pool y de los datos.

**Qué aprenderás:**
- Estadísticas del pool en tiempo real
- Funciones de agregación (COUNT, AVG, MIN, MAX)
- GROUP BY en SQL
- Análisis de datos

#### 9. Configuración personalizada del pool (Solo Python)
Crea una instancia de JVDB2 con configuración personalizada.

**Qué aprenderás:**
- Configuración del pool (min/max, timeout, lifetime)
- Configuración del logger (nivel, archivo, consola)
- Verificación de configuración aplicada

#### 10. Manejo de errores y excepciones
Demuestra el sistema de excepciones personalizadas.

**Qué aprenderás:**
- Captura de `ValidationError`/`ValidationException`
- Captura de `QueryError`/`QueryException`
- Manejo de errores de integridad (email duplicado)
- Buenas prácticas de manejo de errores

### 🔧 UTILIDADES

#### 11. Ver logs del sistema
Muestra las últimas 30 líneas del archivo de log.

**Qué encontrarás:**
- Historial de consultas SQL
- Registro de transacciones
- Errores capturados
- Estadísticas de pool

#### 12. Ejecutar TODOS los ejemplos (Solo Python)
Ejecuta todos los ejemplos en secuencia.

## 💡 Consejos de Uso

### Para Aprender
1. **Empieza por el Ejemplo 1**: Familiarízate con la interfaz
2. **Prueba cada opción**: Explora todas las funcionalidades
3. **Lee los logs**: Después de cada operación, revisa los logs (opción 11)
4. **Experimenta**: El menú es seguro, puedes crear y eliminar usuarios de prueba

### Para Desarrolladores
1. **Analiza el código fuente**: Los archivos del menú son excelentes ejemplos de código
   - Python: `examples/python/menu_interactivo_v2.py`
   - PHP: `examples/php/menu_interactivo_v2.php`

2. **Copia fragmentos**: Usa los ejemplos como base para tu propio código

3. **Personaliza**: Modifica el menú para adaptarlo a tus necesidades

### Para Demostración
1. **Ejecuta la opción 12**: Muestra todas las funcionalidades de una vez
2. **Usa la opción 7**: Demuestra el poder de las transacciones
3. **Muestra la opción 8**: Impresiona con estadísticas en tiempo real

## 🎯 Casos de Uso Recomendados

### Práctica de CRUD
```
Ruta sugerida: 1 → 3 → 5 → 6
(Listar → Insertar → Actualizar → Eliminar)
```

### Aprendizaje de Transacciones
```
Ruta sugerida: 7 → 11
(Ver transacciones → Revisar logs)
```

### Optimización de Rendimiento
```
Ruta sugerida: 4 → 8
(Inserción múltiple → Ver estadísticas del pool)
```

### Manejo de Errores
```
Ruta sugerida: 10 → 11
(Ver errores → Revisar logs)
```

## 🔍 Exploración Avanzada

### Modificar Configuración del Pool

Edita el menú para probar diferentes configuraciones:

**Python** (`menu_interactivo_v2.py`):
```python
pool_config = {
    'min_size': 5,      # Más conexiones iniciales
    'max_size': 20,     # Más conexiones máximas
    'max_lifetime': 7200,  # 2 horas
    'timeout': 30       # 30 segundos de espera
}
```

**PHP** (`menu_interactivo_v2.php`):
```php
$poolConfig = [
    'min_size' => 5,
    'max_size' => 20,
    'max_lifetime' => 7200,
    'timeout' => 30
];
```

### Personalizar Logging

**Python**:
```python
log_config = {
    'enabled': True,
    'level': 'DEBUG',     # Más detalle
    'to_file': True,
    'to_console': True    # Ver en consola también
}
```

**PHP**:
```php
$logConfig = [
    'enabled' => true,
    'level' => 'DEBUG',
    'to_file' => true,
    'to_console' => true
];
```

## 📊 Interpretar las Estadísticas

### Estado del Pool
```
Total conexiones: 5
Conexiones disponibles: 3
Conexiones en uso: 2
```

- **Total**: Número de conexiones creadas en el pool
- **Disponibles**: Conexiones listas para usar
- **En uso**: Conexiones actualmente utilizadas

### Logs del Sistema

Ejemplo de entrada de log:
```
2026-03-09 22:50:03 - JVDB2 - INFO - SQL: SELECT * FROM usuarios WHERE Activo = %s
2026-03-09 22:50:03 - JVDB2 - INFO - Seleccionados 4 registros de 'usuarios'
```

- **Timestamp**: Fecha y hora de la operación
- **Componente**: Módulo que generó el log (JVDB2, Pool, etc.)
- **Nivel**: INFO, DEBUG, WARNING, ERROR, CRITICAL
- **Mensaje**: Descripción de la operación

## ❓ Solución de Problemas

### Error: Tabla 'usuarios' no existe
```
❌ Error: Table 'jvdataaccess_demo.usuarios' doesn't exist
```

**Solución**:
```bash
python crear_tabla_usuarios.py
# o
php crear_tabla_usuarios.php
```

### Error: Credenciales incorrectas
```
❌ Error: Access denied for user 'usuario'@'localhost'
```

**Solución**:
- Verifica `config.py` o `config.php`
- Asegúrate de que las credenciales sean correctas
- Verifica que el servidor MySQL esté activo

### Error: No se puede conectar al servidor
```
❌ Error: Can't connect to MySQL server
```

**Solución**:
- Inicia el servidor MySQL (XAMPP, WAMP, etc.)
- Verifica que el puerto 3306 esté libre
- Comprueba el firewall

## 🎓 Siguiente Paso

Después de explorar el menú interactivo, consulta:

- **[GUIA_V2.md](GUIA_V2.md)**: Documentación completa de la API
- **[MIGRACION_V2.md](MIGRACION_V2.md)**: Si vienes de la v1.0
- **[VERSION_2.0.md](../VERSION_2.0.md)**: Resumen de la implementación

## 📝 Notas Adicionales

- El menú es completamente seguro para experimentar
- Los usuarios de prueba (emails con 'test') se pueden eliminar fácilmente
- Los logs se guardan en `logs/jvdb.log`
- Puedes ejecutar el menú tantas veces como quieras
- Es compatible con Python 3.7+ y PHP 8.0+

## 🤝 Contribuciones

¿Tienes ideas para mejorar el menú? ¡Son bienvenidas!

- Agrega nuevos ejemplos
- Mejora la interfaz
- Traduce a otros idiomas
- Crea tutoriales en video

---

**¡Disfruta explorando JVDataAccess v2.0!** 🚀
