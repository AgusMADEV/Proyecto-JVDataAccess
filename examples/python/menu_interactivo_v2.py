"""
Menú Interactivo de JVDataAccess - Versión 2.0
Fusión de la interfaz de menú de v1.0 con las capacidades mejoradas de v2.0

Características v2.0:
- Pool de conexiones
- Sistema de logging avanzado
- Transacciones automáticas
- Excepciones personalizadas
- Métodos CRUD optimizados
"""

import sys
import os

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'python'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from jvdb.jvdb2 import JVDB2
from jvdb.exceptions import QueryError, ValidationError, TransactionError, ConnectionError as JVConnectionError
from config import DB_CONFIG


def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    """Pausa la ejecución esperando input del usuario"""
    input("\n⏸️  Presiona ENTER para continuar...")


def ejemplo_listado_basico():
    """Ejemplo 1: Listado básico de registros con JVDB2"""
    limpiar_pantalla()
    print("=" * 80)
    print("📚 EJEMPLO 1: Listado básico de registros")
    print("=" * 80)
    
    with JVDB2(
        DB_CONFIG['host'],
        DB_CONFIG['user'],
        DB_CONFIG['password'],
        DB_CONFIG['database']
    ) as db:
        try:
            # Mostrar estadísticas del pool
            print("\n🔄 Estado del Pool de Conexiones:")
            stats = db.pool.get_stats() if db.pool else {"total_connections": 0, "available": 0, "in_use": 0}
            print(f"   Total: {stats['total_connections']} | Disponibles: {stats['available']} | En uso: {stats['in_use']}")
            
            # Listar usuarios
            print("\n👥 USUARIOS:")
            print("-" * 80)
            usuarios = db.seleccionar('usuarios', order_by='Apellido ASC', limit=10)
            
            if usuarios:
                for usuario in usuarios:
                    estado = "✅ Activo" if usuario.get('Activo', 0) == 1 else "❌ Inactivo"
                    print(f"  {usuario['Nombre']} {usuario['Apellido']} - {usuario['Email']} - {estado}")
                print(f"\n📊 Total: {len(usuarios)} usuario(s)")
            else:
                print("  ℹ️  No hay usuarios registrados")
            
            # Listar productos
            print("\n🛍️  PRODUCTOS:")
            print("-" * 80)
            productos = db.seleccionar('productos', columnas='nombre, precio, stock', limit=5)
            
            if productos:
                for producto in productos:
                    print(f"  {producto['nombre']} - ${producto['precio']:.2f} (Stock: {producto['stock']})")
                
                # Usar el nuevo método contar()
                total = db.contar('productos')
                print(f"\n📊 Total: {total} producto(s) en la base de datos")
            else:
                print("  ℹ️  No hay productos registrados")
                
        except QueryError as e:
            print(f"\n❌ Error en consulta: {e}")
    
    pausar()


def ejemplo_busqueda_avanzada():
    """Ejemplo 2: Búsquedas avanzadas con filtros"""
    limpiar_pantalla()
    print("=" * 80)
    print("🔍 EJEMPLO 2: Búsquedas avanzadas con filtros")
    print("=" * 80)
    
    with JVDB2(
        DB_CONFIG['host'],
        DB_CONFIG['user'],
        DB_CONFIG['password'],
        DB_CONFIG['database']
    ) as db:
        try:
            # Búsqueda con WHERE
            print("\n1️⃣  Buscar usuarios activos:")
            print("-" * 40)
            activos = db.seleccionar(
                'usuarios',
                where={'Activo': 1},
                order_by='Nombre ASC'
            )
            
            if activos:
                for usuario in activos:
                    print(f"  ✅ {usuario['Nombre']} {usuario['Apellido']} - {usuario['Email']}")
                print(f"\n📊 {len(activos)} usuario(s) activo(s)")
            else:
                print("  ℹ️  No hay usuarios activos")
            
            # Búsqueda con múltiples condiciones
            print("\n2️⃣  Buscar usuarios mayores de 25 años:")
            print("-" * 40)
            mayores = db.consulta_personalizada(
                "SELECT * FROM usuarios WHERE Edad > %s AND Activo = %s ORDER BY Edad DESC",
                params=(25, 1),
                fetch="all"
            )
            
            if mayores:
                for usuario in mayores:
                    print(f"  👤 {usuario['Nombre']} {usuario['Apellido']} - {usuario['Edad']} años")
            else:
                print("  ℹ️  No hay usuarios que cumplan el criterio")
            
            # Usar el método existe()
            print("\n3️⃣  Verificar si existe un email:")
            print("-" * 40)
            email_buscar = input("  Ingresa un email para buscar: ").strip()
            
            if email_buscar:
                existe = db.existe('usuarios', where={'Email': email_buscar})
                if existe:
                    print(f"  ✅ El email '{email_buscar}' está registrado")
                else:
                    print(f"  ❌ El email '{email_buscar}' NO está registrado")
            
        except QueryError as e:
            print(f"\n❌ Error en consulta: {e}")
    
    pausar()


def ejemplo_insercion():
    """Ejemplo 3: Inserción de registros"""
    limpiar_pantalla()
    print("=" * 80)
    print("➕ EJEMPLO 3: Inserción de registros")
    print("=" * 80)
    
    with JVDB2(
        DB_CONFIG['host'],
        DB_CONFIG['user'],
        DB_CONFIG['password'],
        DB_CONFIG['database']
    ) as db:
        try:
            print("\n📝 Ingresa los datos del nuevo usuario:")
            print("-" * 40)
            
            nombre = input("  Nombre: ").strip()
            apellido = input("  Apellido: ").strip()
            email = input("  Email: ").strip()
            edad = input("  Edad: ").strip()
            
            if not all([nombre, apellido, email, edad]):
                print("\n⚠️  Todos los campos son obligatorios")
                pausar()
                return
            
            # Verificar si el email ya existe
            if db.existe('usuarios', where={'Email': email}):
                print(f"\n⚠️  El email '{email}' ya está registrado")
                pausar()
                return
            
            # Insertar con return_id
            nuevo_usuario = {
                'Nombre': nombre,
                'Apellido': apellido,
                'Email': email,
                'Edad': int(edad),
                'Activo': 1
            }
            
            print("\n⏳ Insertando usuario...")
            resultado = db.insertar('usuarios', nuevo_usuario, return_id=True)
            
            print(f"\n✅ Usuario insertado exitosamente")
            print(f"   ID: {resultado.get('last_insert_id', 'N/A')}")
            print(f"   Filas afectadas: {resultado.get('rows_affected', 0)}")
            
            # Verificar la inserción
            total = db.contar('usuarios', where={'Activo': 1})
            print(f"\n📊 Total de usuarios activos: {total}")
            
        except ValidationError as e:
            print(f"\n❌ Error de validación: {e}")
        except QueryError as e:
            print(f"\n❌ Error en inserción: {e}")
        except ValueError:
            print("\n❌ La edad debe ser un número válido")
    
    pausar()


def ejemplo_insercion_multiple():
    """Ejemplo 4: Inserción múltiple con transacción automática"""
    limpiar_pantalla()
    print("=" * 80)
    print("➕➕ EJEMPLO 4: Inserción múltiple (batch insert)")
    print("=" * 80)
    
    with JVDB2(
        DB_CONFIG['host'],
        DB_CONFIG['user'],
        DB_CONFIG['password'],
        DB_CONFIG['database']
    ) as db:
        try:
            print("\n📝 Insertando 3 usuarios de prueba...")
            print("-" * 40)
            
            usuarios_test = [
                {
                    'Nombre': 'Test1',
                    'Apellido': 'Usuario1',
                    'Email': f'test1_{os.urandom(4).hex()}@test.com',
                    'Edad': 25,
                    'Activo': 1
                },
                {
                    'Nombre': 'Test2',
                    'Apellido': 'Usuario2',
                    'Email': f'test2_{os.urandom(4).hex()}@test.com',
                    'Edad': 30,
                    'Activo': 1
                },
                {
                    'Nombre': 'Test3',
                    'Apellido': 'Usuario3',
                    'Email': f'test3_{os.urandom(4).hex()}@test.com',
                    'Edad': 35,
                    'Activo': 1
                }
            ]
            
            # Inserción múltiple con transacción automática
            filas_insertadas = db.insertar_multiple('usuarios', usuarios_test)
            
            print(f"\n✅ {filas_insertadas} usuario(s) insertado(s) exitosamente")
            print("   ℹ️  La transacción se realizó automáticamente")
            
            # Mostrar los usuarios insertados
            print("\n👥 Usuarios de prueba insertados:")
            for usuario in usuarios_test:
                print(f"   - {usuario['Nombre']} {usuario['Apellido']} ({usuario['Email']})")
            
            # Preguntar si desea eliminarlos
            print("\n" + "-" * 40)
            eliminar = input("¿Deseas eliminar estos usuarios de prueba? (s/n): ").strip().lower()
            
            if eliminar == 's':
                print("\n⏳ Eliminando usuarios de prueba...")
                for usuario in usuarios_test:
                    db.eliminar('usuarios', where={'Email': usuario['Email']})
                print("✅ Usuarios de prueba eliminados")
            
        except QueryError as e:
            print(f"\n❌ Error en inserción múltiple: {e}")
    
    pausar()


def ejemplo_actualizacion():
    """Ejemplo 5: Actualización de registros"""
    limpiar_pantalla()
    print("=" * 80)
    print("✏️  EJEMPLO 5: Actualización de registros")
    print("=" * 80)
    
    with JVDB2(
        DB_CONFIG['host'],
        DB_CONFIG['user'],
        DB_CONFIG['password'],
        DB_CONFIG['database']
    ) as db:
        try:
            # Listar usuarios actuales
            print("\n👥 Usuarios actuales:")
            print("-" * 40)
            usuarios = db.seleccionar('usuarios', limit=10)
            
            if not usuarios:
                print("  ℹ️  No hay usuarios para actualizar")
                pausar()
                return
            
            for i, usuario in enumerate(usuarios, 1):
                estado = "✅" if usuario.get('Activo', 0) == 1 else "❌"
                print(f"  {i}. {usuario['Nombre']} {usuario['Apellido']} - {usuario['Email']} {estado}")
            
            # Seleccionar usuario
            print("\n" + "-" * 40)
            seleccion = input("Selecciona el número de usuario a actualizar (0 para cancelar): ").strip()
            
            if not seleccion.isdigit() or int(seleccion) < 1 or int(seleccion) > len(usuarios):
                print("\n⚠️  Selección inválida")
                pausar()
                return
            
            usuario_seleccionado = usuarios[int(seleccion) - 1]
            
            print(f"\n📝 Actualizando: {usuario_seleccionado['Nombre']} {usuario_seleccionado['Apellido']}")
            print("-" * 40)
            
            print("\n¿Qué deseas actualizar?")
            print("  1. Cambiar estado (Activo/Inactivo)")
            print("  2. Cambiar edad")
            print("  3. Cambiar email")
            
            opcion = input("\n👉 Opción: ").strip()
            
            if opcion == '1':
                nuevo_estado = 0 if usuario_seleccionado.get('Activo', 0) == 1 else 1
                filas = db.actualizar(
                    'usuarios',
                    {'Activo': nuevo_estado},
                    where={'Email': usuario_seleccionado['Email']}
                )
                estado_texto = "Activo" if nuevo_estado == 1 else "Inactivo"
                print(f"\n✅ Usuario actualizado a: {estado_texto}")
                print(f"   Filas afectadas: {filas}")
                
            elif opcion == '2':
                nueva_edad = input("  Nueva edad: ").strip()
                if nueva_edad.isdigit():
                    filas = db.actualizar(
                        'usuarios',
                        {'Edad': int(nueva_edad)},
                        where={'Email': usuario_seleccionado['Email']}
                    )
                    print(f"\n✅ Edad actualizada a: {nueva_edad}")
                    print(f"   Filas afectadas: {filas}")
                else:
                    print("\n❌ Edad inválida")
                    
            elif opcion == '3':
                nuevo_email = input("  Nuevo email: ").strip()
                if nuevo_email and '@' in nuevo_email:
                    # Verificar si el nuevo email ya existe
                    if db.existe('usuarios', where={'Email': nuevo_email}):
                        print(f"\n⚠️  El email '{nuevo_email}' ya está registrado")
                    else:
                        filas = db.actualizar(
                            'usuarios',
                            {'Email': nuevo_email},
                            where={'Email': usuario_seleccionado['Email']}
                        )
                        print(f"\n✅ Email actualizado")
                        print(f"   Filas afectadas: {filas}")
                else:
                    print("\n❌ Email inválido")
            else:
                print("\n⚠️  Opción inválida")
            
        except ValidationError as e:
            print(f"\n❌ Error de validación: {e}")
        except QueryError as e:
            print(f"\n❌ Error en actualización: {e}")
    
    pausar()


def ejemplo_eliminacion():
    """Ejemplo 6: Eliminación de registros"""
    limpiar_pantalla()
    print("=" * 80)
    print("🗑️  EJEMPLO 6: Eliminación de registros")
    print("=" * 80)
    
    with JVDB2(
        DB_CONFIG['host'],
        DB_CONFIG['user'],
        DB_CONFIG['password'],
        DB_CONFIG['database']
    ) as db:
        try:
            # Buscar usuarios de prueba (emails que contengan 'test')
            print("\n🔍 Buscando usuarios de prueba (emails con 'test')...")
            print("-" * 40)
            
            usuarios_test = db.consulta_personalizada(
                "SELECT * FROM usuarios WHERE Email LIKE %s",
                params=('%test%',),
                fetch="all"
            )
            
            if not usuarios_test:
                print("  ℹ️  No hay usuarios de prueba para eliminar")
                print("\n💡 Puedes crear usuarios de prueba con el Ejemplo 4")
                pausar()
                return
            
            print(f"\n👥 Encontrados {len(usuarios_test)} usuario(s) de prueba:")
            for usuario in usuarios_test:
                print(f"   - {usuario['Nombre']} {usuario['Apellido']} ({usuario['Email']})")
            
            print("\n" + "-" * 40)
            confirmar = input("¿Deseas eliminar TODOS estos usuarios? (s/n): ").strip().lower()
            
            if confirmar == 's':
                print("\n⏳ Eliminando usuarios...")
                total_eliminados = 0
                
                for usuario in usuarios_test:
                    filas = db.eliminar('usuarios', where={'Email': usuario['Email']})
                    total_eliminados += filas if filas else 0
                
                print(f"\n✅ {total_eliminados} usuario(s) eliminado(s) exitosamente")
                
                # Verificar
                restantes = db.contar('usuarios')
                print(f"📊 Usuarios restantes en la base de datos: {restantes}")
            else:
                print("\n⏸️  Operación cancelada")
            
        except QueryError as e:
            print(f"\n❌ Error en eliminación: {e}")
    
    pausar()


def ejemplo_transacciones():
    """Ejemplo 7: Transacciones con rollback automático"""
    limpiar_pantalla()
    print("=" * 80)
    print("🔄 EJEMPLO 7: Transacciones con rollback automático")
    print("=" * 80)
    
    with JVDB2(
        DB_CONFIG['host'],
        DB_CONFIG['user'],
        DB_CONFIG['password'],
        DB_CONFIG['database']
    ) as db:
        try:
            print("\n📝 Demostración de transacción con rollback")
            print("-" * 40)
            
            # Contar usuarios actuales
            usuarios_antes = db.contar('usuarios')
            print(f"\n🔢 Usuarios antes de la transacción: {usuarios_antes}")
            
            print("\n⏳ Iniciando transacción...")
            print("   1. Insertando usuario temporal")
            print("   2. Simulando un error")
            print("   3. Rollback automático")
            
            try:
                with db.transaction() as conn:
                    # Insertar un usuario
                    usuario_temporal = {
                        'Nombre': 'Temporal',
                        'Apellido': 'Rollback',
                        'Email': 'temporal@rollback.com',
                        'Edad': 99,
                        'Activo': 1
                    }
                    db.insertar('usuarios', usuario_temporal)
                    print("\n   ✅ Usuario temporal insertado")
                    
                    # Verificar que existe (dentro de la transacción)
                    usuarios_durante = db.contar('usuarios')
                    print(f"   🔢 Usuarios durante la transacción: {usuarios_durante}")
                    
                    # Simular un error
                    print("\n   ⚠️  Simulando error...")
                    raise Exception("Error simulado para demostrar rollback")
                    
            except Exception as e:
                print(f"   ❌ Error capturado: {e}")
                print("   🔄 Rollback ejecutado automáticamente")
            
            # Verificar después del rollback
            usuarios_despues = db.contar('usuarios')
            print(f"\n🔢 Usuarios después del rollback: {usuarios_despues}")
            
            if usuarios_antes == usuarios_despues:
                print("\n✅ ¡Rollback exitoso! Los datos no fueron modificados")
            else:
                print("\n⚠️  Advertencia: Hubo cambios inesperados")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    pausar()


def ejemplo_estadisticas():
    """Ejemplo 8: Estadísticas y agregaciones"""
    limpiar_pantalla()
    print("=" * 80)
    print("📊 EJEMPLO 8: Estadísticas y agregaciones")
    print("=" * 80)
    
    with JVDB2(
        DB_CONFIG['host'],
        DB_CONFIG['user'],
        DB_CONFIG['password'],
        DB_CONFIG['database']
    ) as db:
        try:
            # Estadísticas del pool
            print("\n🔄 ESTADO DEL POOL DE CONEXIONES:")
            print("-" * 40)
            if db.pool:
                stats = db.pool.get_stats()
                print(f"  Total de conexiones: {stats['total_connections']}")
                print(f"  Conexiones disponibles: {stats['available']}")
                print(f"  Conexiones en uso: {stats['in_use']}")
            else:
                print("  ℹ️  Pool no configurado (conexión directa)")
            
            # Estadísticas de usuarios
            print("\n👥 ESTADÍSTICAS DE USUARIOS:")
            print("-" * 40)
            
            total_usuarios = db.contar('usuarios')
            usuarios_activos = db.contar('usuarios', where={'Activo': 1})
            usuarios_inactivos = total_usuarios - usuarios_activos
            
            print(f"  Total de usuarios: {total_usuarios}")
            print(f"  Usuarios activos: {usuarios_activos} ({usuarios_activos/total_usuarios*100:.1f}%)" if total_usuarios > 0 else "  Usuarios activos: 0")
            print(f"  Usuarios inactivos: {usuarios_inactivos} ({usuarios_inactivos/total_usuarios*100:.1f}%)" if total_usuarios > 0 else "  Usuarios inactivos: 0")
            
            # Edad promedio
            resultado = db.consulta_personalizada(
                "SELECT AVG(Edad) as edad_promedio, MIN(Edad) as edad_min, MAX(Edad) as edad_max FROM usuarios WHERE Edad IS NOT NULL",
                fetch="one"
            )
            
            if resultado and resultado['edad_promedio']:
                print(f"\n📈 ANÁLISIS DE EDADES:")
                print("-" * 40)
                print(f"  Edad promedio: {resultado['edad_promedio']:.1f} años")
                print(f"  Edad mínima: {resultado['edad_min']} años")
                print(f"  Edad máxima: {resultado['edad_max']} años")
            
            # Usuarios por estado
            print(f"\n📋 DISTRIBUCIÓN POR ESTADO:")
            print("-" * 40)
            resultado = db.consulta_personalizada(
                "SELECT Activo, COUNT(*) as total FROM usuarios GROUP BY Activo",
                fetch="all"
            )
            
            if resultado:
                for fila in resultado:
                    estado = "Activos" if fila['Activo'] == 1 else "Inactivos"
                    print(f"  {estado}: {fila['total']}")
            
        except QueryError as e:
            print(f"\n❌ Error en consulta: {e}")
    
    pausar()


def ejemplo_configuracion_pool():
    """Ejemplo 9: Configuración personalizada del pool"""
    limpiar_pantalla()
    print("=" * 80)
    print("⚙️  EJEMPLO 9: Configuración personalizada del pool")
    print("=" * 80)
    
    print("\n📝 Configurando pool personalizado...")
    print("-" * 40)
    
    # Configuración del pool
    pool_config = {
        'min_size': 3,
        'max_size': 10,
        'max_lifetime': 3600,  # 1 hora
        'timeout': 10
    }
    
    print(f"  Conexiones mínimas: {pool_config['min_size']}")
    print(f"  Conexiones máximas: {pool_config['max_size']}")
    print(f"  Tiempo de vida máximo: {pool_config['max_lifetime']}s")
    print(f"  Timeout: {pool_config['timeout']}s")
    
    # Configuración del logger
    log_config = {
        'enabled': True,
        'level': 'INFO',
        'to_file': True,
        'to_console': False
    }
    
    print(f"\n📋 Logging configurado:")
    print(f"  Nivel: {log_config['level']}")
    print(f"  Archivo: {'Sí' if log_config['to_file'] else 'No'}")
    print(f"  Consola: {'Sí' if log_config['to_console'] else 'No'}")
    
    try:
        with JVDB2(
            DB_CONFIG['host'],
            DB_CONFIG['user'],
            DB_CONFIG['password'],
            DB_CONFIG['database'],
            pool_config=pool_config,
            log_config=log_config
        ) as db:
            print("\n✅ Conexión establecida con configuración personalizada")
            
            # Mostrar estado del pool
            if db.pool:
                stats = db.pool.get_stats()
                print(f"\n📊 Estado actual del pool:")
                print(f"  Total: {stats['total_connections']}")
                print(f"  Disponibles: {stats['available']}")
                print(f"  En uso: {stats['in_use']}")
            
            # Realizar una consulta simple
            print("\n🔍 Realizando consulta de prueba...")
            total = db.contar('usuarios')
            print(f"✅ Consulta exitosa: {total} usuarios encontrados")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    pausar()


def ejemplo_manejo_errores():
    """Ejemplo 10: Manejo de errores y excepciones"""
    limpiar_pantalla()
    print("=" * 80)
    print("⚠️  EJEMPLO 10: Manejo de errores y excepciones")
    print("=" * 80)
    
    with JVDB2(
        DB_CONFIG['host'],
        DB_CONFIG['user'],
        DB_CONFIG['password'],
        DB_CONFIG['database']
    ) as db:
        # Error 1: Insertar sin datos
        print("\n1️⃣  Error de validación - Insertar sin datos:")
        print("-" * 40)
        try:
            db.insertar('usuarios', {})
        except (ValidationError, QueryError) as e:
            print(f"  ✅ Error capturado correctamente: {e}")
        
        # Error 2: Tabla inexistente
        print("\n2️⃣  Error de consulta - Tabla inexistente:")
        print("-" * 40)
        try:
            db.seleccionar('tabla_que_no_existe')
        except QueryError as e:
            print(f"  ✅ Error capturado correctamente")
            print(f"     Tipo: QueryError")
        
        # Error 3: Email duplicado
        print("\n3️⃣  Error de integridad - Email duplicado:")
        print("-" * 40)
        try:
            # Obtener un email existente
            usuarios = db.seleccionar('usuarios', limit=1)
            if usuarios:
                email_existente = usuarios[0]['Email']
                
                # Intentar insertar con el mismo email
                usuario_duplicado = {
                    'Nombre': 'Duplicado',
                    'Apellido': 'Test',
                    'Email': email_existente,
                    'Edad': 25,
                    'Activo': 1
                }
                db.insertar('usuarios', usuario_duplicado)
            else:
                print("  ℹ️  No hay usuarios para probar este error")
        except QueryError as e:
            print(f"  ✅ Error capturado correctamente")
            print(f"     Email duplicado no permitido")
        
        print("\n✅ Todos los errores manejados correctamente")
        print("   ℹ️  JVDB2 utiliza excepciones personalizadas para mejor control")
    
    pausar()


def ver_logs():
    """Ver los últimos registros del log"""
    limpiar_pantalla()
    print("=" * 80)
    print("📋 LOGS DEL SISTEMA")
    print("=" * 80)
    
    log_file = os.path.join(
        os.path.dirname(__file__),
        '..', '..', 'logs', 'jvdb.log'
    )
    
    if os.path.exists(log_file):
        print(f"\n📁 Archivo: {log_file}")
        print("-" * 80)
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                ultimas_lineas = lines[-30:]  # Últimas 30 líneas
                
                print("\n🔍 Últimas 30 líneas del log:\n")
                for line in ultimas_lineas:
                    print(line.rstrip())
        except Exception as e:
            print(f"\n❌ Error al leer el log: {e}")
    else:
        print("\n⚠️  No se encontró el archivo de log")
        print("   Ejecuta algunos ejemplos primero para generar logs")
    
    pausar()


def menu_principal():
    """Menú interactivo principal"""
    while True:
        limpiar_pantalla()
        print("\n" + "=" * 80)
        print("🚀 JVDataAccess v2.0 - Menú Interactivo")
        print("=" * 80)
        print("\n📚 EJEMPLOS CRUD BÁSICOS:")
        print("  1.  Listado básico de registros")
        print("  2.  Búsquedas avanzadas con filtros")
        print("  3.  Inserción de un registro")
        print("  4.  Inserción múltiple (batch)")
        print("  5.  Actualización de registros")
        print("  6.  Eliminación de registros")
        
        print("\n⚙️  FUNCIONALIDADES AVANZADAS:")
        print("  7.  Demostración de transacciones")
        print("  8.  Estadísticas y agregaciones")
        print("  9.  Configuración personalizada del pool")
        print("  10. Manejo de errores")
        
        print("\n🔧 UTILIDADES:")
        print("  11. Ver logs del sistema")
        print("  12. Ejecutar TODOS los ejemplos")
        
        print("\n  0.  Salir")
        print("-" * 80)
        
        opcion = input("\n👉 Selecciona una opción: ").strip()
        
        if opcion == '1':
            ejemplo_listado_basico()
        elif opcion == '2':
            ejemplo_busqueda_avanzada()
        elif opcion == '3':
            ejemplo_insercion()
        elif opcion == '4':
            ejemplo_insercion_multiple()
        elif opcion == '5':
            ejemplo_actualizacion()
        elif opcion == '6':
            ejemplo_eliminacion()
        elif opcion == '7':
            ejemplo_transacciones()
        elif opcion == '8':
            ejemplo_estadisticas()
        elif opcion == '9':
            ejemplo_configuracion_pool()
        elif opcion == '10':
            ejemplo_manejo_errores()
        elif opcion == '11':
            ver_logs()
        elif opcion == '12':
            print("\n⏳ Ejecutando todos los ejemplos...")
            for func in [
                ejemplo_listado_basico, ejemplo_busqueda_avanzada,
                ejemplo_insercion, ejemplo_insercion_multiple,
                ejemplo_actualizacion, ejemplo_eliminacion,
                ejemplo_transacciones, ejemplo_estadisticas,
                ejemplo_configuracion_pool, ejemplo_manejo_errores
            ]:
                func()
            print("\n✅ Todos los ejemplos completados")
            pausar()
        elif opcion == '0':
            limpiar_pantalla()
            print("\n" + "=" * 80)
            print("👋 ¡Gracias por usar JVDataAccess v2.0!")
            print("=" * 80)
            print("\n📚 Recursos:")
            print("  - Documentación: docs/GUIA_V2.md")
            print("  - Logs: logs/jvdb.log")
            print("  - GitHub: [Tu repositorio]")
            print("\n")
            break
        else:
            print("\n❌ Opción no válida")
            pausar()


if __name__ == "__main__":
    limpiar_pantalla()
    print("\n" + "=" * 80)
    print("🚀 JVDataAccess v2.0 - Sistema de Gestión de Base de Datos")
    print("=" * 80)
    print("\n✨ Características:")
    print("  ✅ Pool de conexiones para mejor rendimiento")
    print("  ✅ Sistema de logging avanzado")
    print("  ✅ Transacciones con rollback automático")
    print("  ✅ Excepciones personalizadas")
    print("  ✅ Métodos CRUD optimizados")
    
    print("\n⚠️  REQUISITOS:")
    print("  1. Base de datos configurada (ejecuta: python crear_tabla_usuarios.py)")
    print("  2. Credenciales en config.py actualizadas")
    print("  3. Tabla 'usuarios' creada")
    
    print("\n" + "-" * 80)
    respuesta = input("\n¿Continuar? (s/n): ").strip().lower()
    
    if respuesta == 's':
        try:
            menu_principal()
        except KeyboardInterrupt:
            print("\n\n⚠️  Programa interrumpido por el usuario")
            print("👋 ¡Hasta luego!\n")
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\n👋 ¡Hasta luego!\n")
