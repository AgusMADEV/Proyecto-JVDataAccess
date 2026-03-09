# 📖 Guía de Inicio Rápido - JVDataAccess

## 🚀 Instalación y Configuración

### Requisitos Previos

#### Python
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

#### PHP
- PHP 7.4 o superior
- Extensión MySQLi habilitada

#### Base de Datos
- MySQL 5.7 o superior / MariaDB 10.3 o superior
- Acceso con permisos de creación de bases de datos

---

## ⚙️ Instalación

### Paso 1: Clonar o Descargar el Proyecto

```bash
# Si estás usando git
git clone [url-del-repo] JVDataAccess

# O simplemente descarga la carpeta del proyecto
```

### Paso 2: Instalar Dependencias

#### Para Python:
```bash
cd JVDataAccess
pip install -r requirements.txt
```

#### Para PHP:
No se requieren dependencias externas, solo asegúrate de que MySQLi esté habilitado:
```bash
php -m | grep mysqli
```

### Paso 3: Configurar Base de Datos

1. **Ejecutar el script SQL de inicialización:**

```bash
# Desde MySQL command line
mysql -u root -p < database/init.sql

# O desde phpMyAdmin
# Importar el archivo database/init.sql
```

2. **Configurar credenciales:**

**Python** - Edita `config.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'tu_usuario',      # ⚠️ Cambia esto
    'password': 'tu_password',  # ⚠️ Cambia esto
    'database': 'jvdataaccess_demo',
    'port': 3306
}
```

**PHP** - Edita `config.php`:
```php
define('DB_HOST', 'localhost');
define('DB_USER', 'tu_usuario');      // ⚠️ Cambia esto
define('DB_PASSWORD', 'tu_password'); // ⚠️ Cambia esto
define('DB_NAME', 'jvdataaccess_demo');
define('DB_PORT', 3306);
```

---

## 🎯 Primeros Pasos

### Ejemplo Rápido en Python

```python
from src.python.jvdb import JVDB

# Crear conexión
db = JVDB('localhost', 'usuario', 'password', 'jvdataaccess_demo')

# Consultar datos
productos = db.seleccionar('productos')
print(productos)

# Insertar datos
db.insertar('productos', {
    'nombre': 'Nuevo Producto',
    'precio': 99.99,
    'stock': 10,
    'categoria': 'Electrónica'
})

# Cerrar conexión
db.desconectar()
```

### Ejemplo Rápido en PHP

```php
<?php
require_once 'src/php/JVDB/JVDB.php';
use JVDB\JVDB;

// Crear conexión
$db = new JVDB('localhost', 'usuario', 'password', 'jvdataaccess_demo');

// Consultar datos
$productos = $db->seleccionar('productos');
echo $productos;

// Insertar datos
$db->insertar('productos', [
    'nombre' => 'Nuevo Producto',
    'precio' => 99.99,
    'stock' => 10,
    'categoria' => 'Electrónica'
]);
?>
```

---

## 🧪 Probar los Ejemplos

### Python
```bash
cd examples/python
python ejemplo_basico.py
```

### PHP
```bash
cd examples/php
php ejemplo_basico.php
```

---

## 📚 Documentación Completa

### Estructura de Métodos JVDB

#### Consultas (Read)
- `seleccionar(tabla, columnas='*', formato='json')` - Obtener todos los registros
- `seleccionar_uno(tabla, identificador)` - Obtener un registro por ID
- `buscar(tabla, columna, valor, formato='json')` - Buscar con LIKE
- `consulta_personalizada(query, params, formato)` - Ejecutar SQL personalizado

#### Modificación (Create/Update/Delete)
- `insertar(tabla, datos)` - Insertar nuevo registro
- `actualizar(tabla, identificador, datos)` - Actualizar registro existente
- `eliminar(tabla, identificador)` - Eliminar registro

#### Utilidades
- `tablas(formato='json')` - Listar tablas de la BD
- `estructura_tabla(tabla, formato='json')` - Ver estructura de una tabla
- `conectar()` - Establecer conexión
- `desconectar()` - Cerrar conexión
- `esta_conectado()` - Verificar estado de conexión

---

## 🔧 Solución de Problemas

### Error: "Access denied for user"
**Solución**: Verifica tus credenciales en `config.py` o `config.php`

### Error: "Unknown database"
**Solución**: Ejecuta el script `database/init.sql` para crear la base de datos

### Error: "No module named 'mysql.connector'" (Python)
**Solución**: Ejecuta `pip install -r requirements.txt`

### Error: "Call to undefined function mysqli_connect()" (PHP)
**Solución**: Habilita la extensión MySQLi en tu php.ini

---

## 📞 Soporte

Para preguntas o problemas:
1. Revisa la documentación en `/docs`
2. Consulta los ejemplos en `/examples`
3. Revisa el CHANGELOG.md para cambios recientes

---

## 🎓 Siguiente Paso

Una vez que hayas completado la configuración básica, explora:
- Ejemplos avanzados con JOIN y transacciones
- Query Builder para consultas complejas
- YourSQL para control de bajo nivel
- Prepararte para la Versión 2.0 con nuevas características
