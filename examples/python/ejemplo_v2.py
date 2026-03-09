"""
Ejemplo de uso de JVDB 2.0 - Versión avanzada con pool de conexiones
Versión: 2.0.0

Demuestra las nuevas características de JVDB2:
- Pool de conexiones
- Sistema de logging
- Transacciones
- CRUD optimizado
- Manejo robusto de errores
"""

import sys
import os

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Importar la configuración
from config import DB_CONFIG

# Importar JVDB2
from src.python.jvdb.jvdb2 import JVDB2
from src.python.jvdb.exceptions import *


def ejemplo_basico():
    """Ejemplo básico de uso de JVDB2 con pool"""
    print("=" * 60)
    print("EJEMPLO 1: Uso básico con pool de conexiones")
    print("=" * 60)
    
    # Configuración del pool
    pool_config = {
        'min_size': 2,
        'max_size': 5,
        'max_lifetime': 3600,
        'timeout': 10
    }
    
    # Configuración del logger
    log_config = {
        'log_dir': 'logs',
        'console_output': True,
        'file_output': True
    }
    
    # Crear instancia de JVDB2
    db = JVDB2(
        DB_CONFIG['host'],
        DB_CONFIG['user'],
        DB_CONFIG['password'],
        DB_CONFIG['database'],
        DB_CONFIG['port'],
        use_pool=True,
        pool_config=pool_config,
        log_config=log_config
    )
    
    try:
        # Consulta simple
        usuarios = db.seleccionar('usuarios')
        print(f"\nUsuarios encontrados: {len(usuarios)}")
        for usuario in usuarios[:3]:
            print(f"  - {usuario['Nombre']} {usuario['Apellido']}")
        
        # Estadísticas del pool
        stats = db.get_pool_stats()
        print(f"\nEstadísticas del pool:")
        print(f"  Total conexiones: {stats['total_connections']}")
        print(f"  En uso: {stats['in_use']}")
        print(f"  Disponibles: {stats['available']}")
        
    finally:
        db.cerrar()


def ejemplo_crud_avanzado():
    """Ejemplo de CRUD completo con opciones avanzadas"""
    print("\n" + "=" * 60)
    print("EJEMPLO 2: CRUD avanzado")
    print("=" * 60)
    
    with JVDB2(
        DB_CONFIG['host'],
        DB_CONFIG['user'],
        DB_CONFIG['password'],
        DB_CONFIG['database'],
        use_pool=True
    ) as db:
        
        # SELECT con WHERE, ORDER BY y LIMIT
        print("\n1. SELECT avanzado:")
        usuarios = db.seleccionar(
            'usuarios',
            columnas=['Nombre', 'Apellido', 'Email'],
            where={'Activo': 1},
            order_by='Apellido ASC',
            limit=5
        )
        print(f"   {len(usuarios)} usuarios activos")
        
        # INSERT con return_id
        print("\n2. INSERT con ID retornado:")
        nuevo_usuario = {
            'Nombre': 'Ana',
            'Apellido': 'García',
            'Email': 'ana.garcia@example.com',
            'Edad': 28,
            'Activo': 1
        }
        resultado = db.insertar('usuarios', nuevo_usuario, return_id=True)
        print(f"   Insertado ID: {resultado.get('last_insert_id')}")
        
        # UPDATE con WHERE personalizado
        print("\n3. UPDATE con condiciones:")
        filas = db.actualizar(
            'usuarios',
            datos={'Activo': 0},
            where={'Email': 'ana.garcia@example.com'}
        )
        print(f"   {filas} fila(s) actualizada(s)")
        
        # COUNT
        print("\n4. COUNT:")
        total = db.contar('usuarios')
        activos = db.contar('usuarios', where={'Activo': 1})
        print(f"   Total usuarios: {total}")
        print(f"   Usuarios activos: {activos}")
        
        # EXISTS
        print("\n5. EXISTS:")
        existe = db.existe('usuarios', {'Email': 'ana.garcia@example.com'})
        print(f"   ¿Existe el email?: {existe}")
        
        # DELETE
        print("\n6. DELETE:")
        eliminados = db.eliminar('usuarios', where={'Email': 'ana.garcia@example.com'})
        print(f"   {eliminados} registro(s) eliminado(s)")


def ejemplo_transacciones():
    """Ejemplo de uso de transacciones"""
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Transacciones")
    print("=" * 60)
    
    db = JVDB2(
        DB_CONFIG['host'],
        DB_CONFIG['user'],
        DB_CONFIG['password'],
        DB_CONFIG['database'],
        use_pool=True
    )
    
    try:
        print("\nInsertando múltiples registros en transacción...")
        
        with db.transaction():
            # Insertar varios usuarios
            usuarios = [
                {'Nombre': 'Carlos', 'Apellido': 'López', 'Email': 'carlos@test.com', 'Edad': 35, 'Activo': 1},
                {'Nombre': 'María', 'Apellido': 'Ruiz', 'Email': 'maria@test.com', 'Edad': 29, 'Activo': 1},
                {'Nombre': 'Pedro', 'Apellido': 'Sanz', 'Email': 'pedro@test.com', 'Edad': 42, 'Activo': 1}
            ]
            
            for usuario in usuarios:
                db.insertar('usuarios', usuario)
        
        print("✅ Transacción completada exitosamente")
        
        # Verificar
        total = db.contar('usuarios', where={'Activo': 1})
        print(f"Total usuarios activos: {total}")
        
        # Ejemplo de rollback
        print("\nProbando rollback...")
        try:
            with db.transaction():
                db.insertar('usuarios', {'Nombre': 'Test', 'Apellido': 'User', 'Email': 'test@test.com', 'Edad': 25, 'Activo': 1})
                # Simular un error
                raise Exception("Error simulado")
        except Exception as e:
            print(f"⚠️  Transacción revertida: {e}")
        
        # Limpiar datos de prueba
        print("\nLimpiando datos de prueba...")
        db.eliminar('usuarios', where={'Email': 'carlos@test.com'})
        db.eliminar('usuarios', where={'Email': 'maria@test.com'})
        db.eliminar('usuarios', where={'Email': 'pedro@test.com'})
        
    finally:
        db.cerrar()


def ejemplo_insercion_multiple():
    """Ejemplo de inserción múltiple optimizada"""
    print("\n" + "=" * 60)
    print("EJEMPLO 4: Inserción múltiple")
    print("=" * 60)
    
    with JVDB2(
        DB_CONFIG['host'],
        DB_CONFIG['user'],
        DB_CONFIG['password'],
        DB_CONFIG['database']
    ) as db:
        
        # Crear múltiples registros
        usuarios = [
            {'Nombre': f'Usuario{i}', 'Apellido': f'Apellido{i}', 
             'Email': f'usuario{i}@test.com', 'Edad': 20+i, 'Activo': 1}
            for i in range(5)
        ]
        
        print(f"\nInsertando {len(usuarios)} usuarios...")
        total = db.insertar_multiple('usuarios', usuarios)
        print(f"✅ {total} registros insertados")
        
        # Limpiar
        print("\nLimpiando registros de prueba...")
        for i in range(5):
            db.eliminar('usuarios', where={'Email': f'usuario{i}@test.com'})


def ejemplo_manejo_errores():
    """Ejemplo de manejo de errores"""
    print("\n" + "=" * 60)
    print("EJEMPLO 5: Manejo de errores")
    print("=" * 60)
    
    db = JVDB2(
        DB_CONFIG['host'],
        DB_CONFIG['user'],
        DB_CONFIG['password'],
        DB_CONFIG['database']
    )
    
    try:
        # Intentar insertar sin datos
        print("\n1. Intentando insertar sin datos:")
        try:
            db.insertar('usuarios', {})
        except QueryError as e:
            print(f"   ✅ QueryError capturado: {e}")
        
        # Intentar actualizar sin condiciones
        print("\n2. Intentando actualizar sin condiciones:")
        try:
            db.actualizar('usuarios', {'Nombre': 'Test'})
        except (ValidationError, QueryError) as e:
            print(f"   ✅ Error capturado: {e}")
        
        # Consulta con tabla inexistente
        print("\n3. Intentando consultar tabla inexistente:")
        try:
            db.seleccionar('tabla_que_no_existe')
        except QueryError as e:
            print(f"   ✅ QueryError capturado")
        
    finally:
        db.cerrar()


def ejemplo_consultas_personalizadas():
    """Ejemplo de consultas SQL personalizadas"""
    print("\n" + "=" * 60)
    print("EJEMPLO 6: Consultas personalizadas")
    print("=" * 60)
    
    with JVDB2(
        DB_CONFIG['host'],
        DB_CONFIG['user'],
        DB_CONFIG['password'],
        DB_CONFIG['database']
    ) as db:
        
        # Consulta con JOIN (si tienes tablas relacionadas)
        print("\n1. Consulta con agregación:")
        resultado = db.consulta_personalizada(
            "SELECT Activo, COUNT(*) as total FROM usuarios GROUP BY Activo",
            fetch="all"
        )
        print("   Usuarios por estado:")
        for row in resultado:
            estado = "Activos" if row['Activo'] == 1 else "Inactivos"
            print(f"   - {estado}: {row['total']}")
        
        # Consulta con parámetros
        print("\n2. Consulta con parámetros:")
        resultado = db.consulta_personalizada(
            "SELECT * FROM usuarios WHERE Edad > %s AND Activo = %s LIMIT 5",
            params=(25, 1),
            fetch="all"
        )
        print(f"   {len(resultado)} usuarios mayores de 25 años")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("DEMOSTRACIONES DE JVDB 2.0")
    print("=" * 60)
    
    try:
        ejemplo_basico()
        ejemplo_crud_avanzado()
        ejemplo_transacciones()
        ejemplo_insercion_multiple()
        ejemplo_manejo_errores()
        ejemplo_consultas_personalizadas()
        
        print("\n" + "=" * 60)
        print("✅ Todos los ejemplos completados")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error en los ejemplos: {e}")
        import traceback
        traceback.print_exc()
