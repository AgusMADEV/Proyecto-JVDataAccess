# 🧪 Guía de Prueba - JVDataAccess v1.0

Esta guía te ayudará a probar el proyecto paso a paso para verificar que todo funciona correctamente.

---

## ✅ Checklist de Pre-requisitos

Antes de comenzar, verifica que tienes:

- [ ] Python 3.8+ instalado (`python --version`)
- [ ] PHP 7.4+ instalado (`php --version`)
- [ ] MySQL/MariaDB instalado y ejecutándose
- [ ] Acceso a la línea de comandos
- [ ] Acceso a la carpeta del proyecto

---

## 📋 Paso 1: Configurar Base de Datos

### 1.1 Crear la base de datos

**Opción A - Desde línea de comandos:**
```bash
# Navega a la carpeta del proyecto
cd "d:\xampp\htdocs\DAM-2\Acceso a datos\301-Actividades final de unidad - Segundo trimestre\002-Clase personalizada de conexión y acceso a datos de vuestra elección\101-Ejercicios\JVDataAccess"

# Ejecuta el script SQL
mysql -u root -p < database/init.sql
```

**Opción B - Desde phpMyAdmin:**
1. Abre phpMyAdmin en tu navegador (normalmente http://localhost/phpmyadmin)
2. Haz clic en "Importar"
3. Selecciona el archivo `database/init.sql`
4. Haz clic en "Continuar"

### 1.2 Verificar que se creó correctamente

```sql
-- Ejecuta esto en MySQL o phpMyAdmin
USE jvdataaccess_demo;
SHOW TABLES;
SELECT COUNT(*) FROM productos;  -- Debe devolver 5
SELECT COUNT(*) FROM clientes;   -- Debe devolver 5
```

**✅ Resultado esperado:**
- Base de datos `jvdataaccess_demo` creada
- 4 tablas: productos, clientes, pedidos, pedidos_detalle
- Datos de ejemplo insertados

---

## 📋 Paso 2: Configurar Credenciales

### 2.1 Editar config.py (Python)

Abre el archivo `config.py` y modifica:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',             # ⚠️ TU USUARIO
    'password': '',             # ⚠️ TU CONTRASEÑA (vacío para root sin password)
    'database': 'jvdataaccess_demo',
    'port': 3306
}
```

### 2.2 Editar config.php (PHP)

Abre el archivo `config.php` y modifica:

```php
define('DB_HOST', 'localhost');
define('DB_USER', 'root');           // ⚠️ TU USUARIO
define('DB_PASSWORD', '');           // ⚠️ TU CONTRASEÑA
define('DB_NAME', 'jvdataaccess_demo');
```

**✅ Guarda ambos archivos**

---

## 📋 Paso 3: Instalar Dependencias Python

```bash
# Desde la carpeta del proyecto
pip install -r requirements.txt
```

**✅ Resultado esperado:**
```
Successfully installed mysql-connector-python-8.3.0
```

---

## 📋 Paso 4: Probar Ejemplos Python

### 4.1 Ejecutar ejemplo básico

```bash
cd examples/python
python ejemplo_basico.py
```

**✅ Resultado esperado:**
- Menú interactivo aparece
- Puedes seleccionar opciones 1-5
- Sin errores de conexión

### 4.2 Probar cada ejemplo

**Opción 1: Uso básico de JVDB**
- Debe listar las tablas
- Mostrar productos
- Insertar nuevo producto
- Sin errores

**Opción 2: Consultas avanzadas**
- Consultas con JOIN funcionan
- Actualizar registros funciona
- Transacciones funcionan

**Opción 3: Uso directo de YourSQL**
- Query directo funciona
- Prepared statements funcionan
- Query Builder funciona

**Opción 4: Context Managers**
- Conexión se abre y cierra automáticamente

### 4.3 Verificar output

Ejemplo de output correcto:
```
================================================================================
📚 EJEMPLO 1: Uso básico de JVDB
================================================================================
✅ Conectado a la base de datos 'jvdataaccess_demo'

1️⃣  Listar tablas de la base de datos:
----------------------------------------
  📋 clientes
  📋 pedidos
  📋 pedidos_detalle
  📋 productos

2️⃣  Consultar todos los productos:
----------------------------------------
  🛍️  Laptop Dell XPS 15 - $1299.99
  🛍️  Mouse Logitech MX Master 3 - $89.99
  🛍️  Teclado Mecánico Corsair K95 - $179.99
...
```

---

## 📋 Paso 5: Probar Ejemplos PHP

### 5.1 Ejecutar ejemplo básico

```bash
cd examples/php
php ejemplo_basico.php
```

**✅ Resultado esperado:**
- Menú interactivo aparece
- Puedes seleccionar opciones 1-4
- Sin errores de conexión

### 5.2 Probar cada ejemplo

Igual que con Python, prueba cada opción del menú.

### 5.3 Verificar output

El output debe ser similar al de Python:
```
================================================================================
📚 EJEMPLO 1: Uso básico de JVDB
================================================================================
✅ Conectado a la base de datos 'jvdataaccess_demo'

1️⃣  Listar tablas de la base de datos:
----------------------------------------
  📋 clientes
  📋 pedidos
...
```

---

## 📋 Paso 6: Pruebas Manuales Adicionales

### 6.1 Crear tu propio script Python

Crea un archivo `test_manual.py`:

```python
import sys
sys.path.insert(0, '../../src/python')

from jvdb import JVDB

# Ajusta estas credenciales
db = JVDB('localhost', 'root', '', 'jvdataaccess_demo')

# Prueba 1: Listar tablas
print("Tablas:", db.tablas(formato='list'))

# Prueba 2: Consultar productos
productos = db.seleccionar('productos', formato='list')
print(f"Total productos: {len(productos)}")

# Prueba 3: Buscar
resultados = db.buscar('productos', 'categoria', 'Audio', formato='list')
print(f"Productos de Audio: {len(resultados)}")

print("✅ Todas las pruebas pasaron")
```

Ejecuta:
```bash
python test_manual.py
```

### 6.2 Crear tu propio script PHP

Crea un archivo `test_manual.php`:

```php
<?php
require_once '../../src/php/JVDB/JVDB.php';
use JVDB\JVDB;

$db = new JVDB('localhost', 'root', '', 'jvdataaccess_demo', 3306, false);
$db->conectar();

// Prueba 1: Listar tablas
$tablas = $db->tablas('array');
echo "Tablas: " . count($tablas) . "\n";

// Prueba 2: Consultar productos
$productos = $db->seleccionar('productos', '*', 'array');
echo "Total productos: " . count($productos) . "\n";

// Prueba 3: Buscar
$resultados = $db->buscar('productos', 'categoria', 'Audio', 'array');
echo "Productos de Audio: " . count($resultados) . "\n";

echo "✅ Todas las pruebas pasaron\n";
?>
```

Ejecuta:
```bash
php test_manual.php
```

---

## 📋 Paso 7: Verificar Estructura del Proyecto

Verifica que tienes todos estos archivos:

```
JVDataAccess/
├── README.md                         ✅
├── CHANGELOG.md                      ✅
├── requirements.txt                  ✅
├── config.py                         ✅
├── config.php                        ✅
├── src/
│   ├── python/
│   │   ├── __init__.py              ✅
│   │   ├── yoursql/
│   │   │   ├── __init__.py         ✅
│   │   │   └── yoursql.py          ✅
│   │   └── jvdb/
│   │       ├── __init__.py         ✅
│   │       └── jvdb.py             ✅
│   └── php/
│       ├── YourSQL/
│       │   └── YourSQL.php         ✅
│       └── JVDB/
│           └── JVDB.php            ✅
├── examples/
│   ├── python/
│   │   └── ejemplo_basico.py       ✅
│   └── php/
│       └── ejemplo_basico.php      ✅
├── database/
│   └── init.sql                     ✅
└── docs/
    ├── GUIA_INICIO.md               ✅
    ├── ROADMAP.md                   ✅
    ├── ESTADO_PROYECTO.md           ✅
    └── GUIA_PRUEBAS.md              ✅ (este archivo)
```

---

## 🐛 Solución de Problemas Comunes

### Error: "Access denied for user"

**Causa**: Credenciales incorrectas

**Solución**:
1. Verifica tu usuario y contraseña de MySQL
2. Actualiza `config.py` y `config.php`
3. Prueba la conexión directamente:
   ```bash
   mysql -u tu_usuario -p
   ```

### Error: "Unknown database 'jvdataaccess_demo'"

**Causa**: Base de datos no creada

**Solución**:
1. Ejecuta el script `database/init.sql`
2. Verifica que se creó: `SHOW DATABASES;`

### Error: "No module named 'mysql.connector'"

**Causa**: Dependencias no instaladas

**Solución**:
```bash
pip install mysql-connector-python
```

### Error: "Call to undefined function mysqli_connect()"

**Causa**: Extensión MySQLi no habilitada en PHP

**Solución**:
1. Edita tu `php.ini`
2. Descomenta la línea: `extension=mysqli`
3. Reinicia tu servidor web/PHP

### Error: "ImportError: attempted relative import with no known parent package"

**Causa**: Imports relativos no funcionan

**Solución**:
- Ejecuta los scripts desde la carpeta correcta
- O usa imports absolutos añadiendo al sys.path

---

## ✅ Checklist Final de Verificación

Marca cada item cuando lo hayas verificado:

### Base de Datos
- [ ] Base de datos `jvdataaccess_demo` existe
- [ ] Tabla `productos` tiene 5 registros
- [ ] Tabla `clientes` tiene 5 registros
- [ ] Tabla `pedidos` tiene 3 registros

### Python
- [ ] `mysql-connector-python` instalado
- [ ] Ejemplo básico ejecuta sin errores
- [ ] Puede listar tablas
- [ ] Puede consultar productos
- [ ] Puede insertar datos
- [ ] Puede actualizar datos

### PHP
- [ ] MySQLi habilitado
- [ ] Ejemplo básico ejecuta sin errores
- [ ] Puede listar tablas
- [ ] Puede consultar productos
- [ ] Puede insertar datos
- [ ] Puede actualizar datos

### Funcionalidades
- [ ] YourSQL conecta correctamente
- [ ] JVDB realiza CRUD
- [ ] Query Builder funciona
- [ ] Prepared statements funcionan
- [ ] Transacciones funcionan
- [ ] Context managers funcionan (Python)

---

## 🎉 ¡Pruebas Completadas!

Si todos los items están marcados, **¡felicidades!** El proyecto JVDataAccess v1.0 está funcionando correctamente.

### Próximos pasos:
1. Experimenta con tus propias consultas
2. Modifica los ejemplos para adaptarlos a tus necesidades
3. Lee la documentación en `/docs` para profundizar
4. Prepárate para la Versión 2.0 con nuevas características

---

## 📝 Reportar Problemas

Si encuentras algún problema no listado aquí:
1. Verifica que seguiste todos los pasos
2. Revisa los mensajes de error cuidadosamente
3. Consulta la documentación en `/docs`
4. Anota el problema para futuras mejoras

---

*Guía de pruebas para JVDataAccess v1.0 - Última actualización: 6 de marzo de 2026*
