"""
Ejemplo básico de uso de JVDataAccess en Python
Versión: 1.0.0

Este ejemplo demuestra las funcionalidades básicas de:
- YourSQL: Conector MySQL personalizado
- JVDB: Clase de abstracción para base de datos
"""

import sys
import os

# Añadir el directorio src al path para importar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'python'))

from jvdb import JVDB
from yoursql import YourSQLConnection, YourSQLQueryBuilder
import json

# Importar configuración
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from config import DB_CONFIG


def ejemplo_jvdb_basico():
    """Ejemplo básico de uso de JVDB"""
    print("=" * 80)
    print("📚 EJEMPLO 1: Uso básico de JVDB")
    print("=" * 80)
    
    # Crear instancia de JVDB
    db = JVDB(
        host=DB_CONFIG['host'],
        usuario=DB_CONFIG['user'],
        contrasena=DB_CONFIG['password'],
        basedatos=DB_CONFIG['database']
    )
    
    # 1. Listar todas las tablas
    print("\n1️⃣  Listar tablas de la base de datos:")
    print("-" * 40)
    tablas = db.tablas(formato='list')
    for tabla in tablas:
        print(f"  📋 {tabla}")
    
    # 2. Consultar productos
    print("\n2️⃣  Consultar todos los productos:")
    print("-" * 40)
    productos = db.seleccionar('productos', formato='list')
    for producto in productos[:3]:  # Mostrar solo 3
        print(f"  🛍️  {producto['nombre']} - ${producto['precio']}")
    
    # 3. Buscar productos por categoría
    print("\n3️⃣  Buscar productos de categoría 'Periféricos':")
    print("-" * 40)
    perifericos = db.buscar('productos', 'categoria', 'Periféricos', formato='list')
    for producto in perifericos:
        print(f"  ⌨️  {producto['nombre']} - Stock: {producto['stock']}")
    
    # 4. Insertar un nuevo producto
    print("\n4️⃣  Insertar nuevo producto:")
    print("-" * 40)
    nuevo_producto = {
        'nombre': 'Webcam Logitech C920',
        'descripcion': 'Cámara web Full HD 1080p',
        'precio': 79.99,
        'stock': 25,
        'categoria': 'Periféricos'
    }
    db.insertar('productos', nuevo_producto)
    
    # 5. Consultar un registro específico
    print("\n5️⃣  Consultar cliente por ID:")
    print("-" * 40)
    cliente = db.seleccionar_uno('clientes', 1)
    if cliente:
        print(f"  👤 {cliente['nombre']} {cliente['apellidos']}")
        print(f"  📧 {cliente['email']}")
    
    # Cerrar conexión
    db.desconectar()
    print("\n✅ Ejemplo completado con éxito\n")


def ejemplo_consultas_avanzadas():
    """Ejemplo de consultas más avanzadas con JVDB"""
    print("=" * 80)
    print("📚 EJEMPLO 2: Consultas avanzadas con JVDB")
    print("=" * 80)
    
    db = JVDB(
        host=DB_CONFIG['host'],
        usuario=DB_CONFIG['user'],
        contrasena=DB_CONFIG['password'],
        basedatos=DB_CONFIG['database']
    )
    
    # 1. Consulta personalizada con JOIN
    print("\n1️⃣  Consulta con JOIN - Pedidos con datos de clientes:")
    print("-" * 60)
    query = """
        SELECT 
            p.Identificador,
            c.nombre,
            c.email,
            p.fecha_pedido,
            p.estado,
            p.total
        FROM pedidos p
        INNER JOIN clientes c ON p.cliente_id = c.Identificador
        ORDER BY p.fecha_pedido DESC
        LIMIT 5
    """
    pedidos = db.consulta_personalizada(query, formato='list')
    for pedido in pedidos:
        print(f"  📦 Pedido #{pedido['Identificador']} - {pedido['nombre']}")
        print(f"     Estado: {pedido['estado']} | Total: ${pedido['total']}")
    
    # 2. Actualizar un producto
    print("\n2️⃣  Actualizar stock de un producto:")
    print("-" * 60)
    db.actualizar('productos', 2, {'stock': 55})
    producto = db.seleccionar_uno('productos', 2)
    print(f"  Stock actualizado: {producto['nombre']} -> {producto['stock']} unidades")
    
    # 3. Estructura de una tabla
    print("\n3️⃣  Ver estructura de tabla 'productos':")
    print("-" * 60)
    estructura = db.estructura_tabla('productos', formato='list')
    for columna in estructura:
        print(f"  🔹 {columna['Field']} - {columna['Type']}")
    
    db.desconectar()
    print("\n✅ Ejemplo completado con éxito\n")


def ejemplo_yoursql_directo():
    """Ejemplo de uso directo de YourSQL"""
    print("=" * 80)
    print("📚 EJEMPLO 3: Uso directo de YourSQL (bajo nivel)")
    print("=" * 80)
    
    # Crear conexión con YourSQL
    conexion = YourSQLConnection(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )
    
    conexion.connect()
    print("\n✅ Conexión establecida con YourSQL\n")
    
    # 1. Query directo
    print("1️⃣  Consulta directa con YourSQL:")
    print("-" * 60)
    resultado = conexion.execute_query("SELECT * FROM productos WHERE precio < 100")
    for producto in resultado:
        print(f"  💰 {producto['nombre']} - ${producto['precio']}")
    
    # 2. Query con parámetros (prepared statement)
    print("\n2️⃣  Consulta preparada con parámetros:")
    print("-" * 60)
    resultado = conexion.execute_query(
        "SELECT * FROM productos WHERE categoria = %s",
        params=('Audio',)
    )
    for producto in resultado:
        print(f"  🎧 {producto['nombre']}")
    
    # 3. Query Builder
    print("\n3️⃣  Uso del Query Builder:")
    print("-" * 60)
    builder = YourSQLQueryBuilder(conexion)
    resultado = (builder
                .select('nombre', 'email', 'ciudad')
                .from_table('clientes')
                .where("ciudad = 'Barcelona'")
                .order_by('nombre', 'ASC')
                .execute())
    
    for cliente in resultado:
        print(f"  🌆 {cliente['nombre']} - {cliente['ciudad']}")
    
    conexion.disconnect()
    print("\n✅ Ejemplo completado con éxito\n")


def ejemplo_context_manager():
    """Ejemplo usando context managers (with statement)"""
    print("=" * 80)
    print("📚 EJEMPLO 4: Uso de Context Managers")
    print("=" * 80)
    
    print("\n💡 Los context managers gestionan automáticamente la conexión\n")
    
    # Usar JVDB con context manager
    with JVDB(
        host=DB_CONFIG['host'],
        usuario=DB_CONFIG['user'],
        contrasena=DB_CONFIG['password'],
        basedatos=DB_CONFIG['database'],
        autoconnect=True
    ) as db:
        print("Dentro del contexto - conexión activa")
        productos = db.seleccionar('productos', columnas='nombre, precio', formato='list')
        print(f"Se obtuvieron {len(productos)} productos")
    
    print("Fuera del contexto - conexión cerrada automáticamente\n")
    print("✅ Ejemplo completado con éxito\n")


def menu_principal():
    """Menú interactivo para ejecutar los ejemplos"""
    while True:
        print("\n" + "=" * 80)
        print("🚀 JVDataAccess - Ejemplos de Uso (Python)")
        print("=" * 80)
        print("\nSelecciona un ejemplo:")
        print("  1. Uso básico de JVDB")
        print("  2. Consultas avanzadas")
        print("  3. Uso directo de YourSQL")
        print("  4. Context Managers")
        print("  5. Ejecutar todos los ejemplos")
        print("  0. Salir")
        print("-" * 80)
        
        opcion = input("\n👉 Opción: ").strip()
        
        if opcion == '1':
            ejemplo_jvdb_basico()
        elif opcion == '2':
            ejemplo_consultas_avanzadas()
        elif opcion == '3':
            ejemplo_yoursql_directo()
        elif opcion == '4':
            ejemplo_context_manager()
        elif opcion == '5':
            ejemplo_jvdb_basico()
            ejemplo_consultas_avanzadas()
            ejemplo_yoursql_directo()
            ejemplo_context_manager()
        elif opcion == '0':
            print("\n👋 ¡Hasta luego!\n")
            break
        else:
            print("\n❌ Opción no válida\n")
        
        input("\nPresiona ENTER para continuar...")


if __name__ == "__main__":
    # Verificar que la base de datos esté configurada
    print("\n⚠️  Asegúrate de haber ejecutado el script database/init.sql primero")
    print("    y de configurar tus credenciales en config.py\n")
    
    respuesta = input("¿Continuar? (s/n): ").strip().lower()
    if respuesta == 's':
        menu_principal()
    else:
        print("\n👋 ¡Hasta luego!\n")
