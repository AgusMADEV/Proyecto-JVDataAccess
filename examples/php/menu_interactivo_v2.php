<?php
/**
 * Menú Interactivo de JVDataAccess - Versión 2.0 (PHP)
 * Fusión de la interfaz de menú de v1.0 con las capacidades mejoradas de v2.0
 * 
 * Características v2.0:
 * - Pool de conexiones
 * - Sistema de logging avanzado
 * - Transacciones automáticas
 * - Excepciones personalizadas
 * - Métodos CRUD optimizados
 */

require_once __DIR__ . '/../../config.php';
require_once __DIR__ . '/../../src/php/YourSQL/YourSQL.php';
require_once __DIR__ . '/../../src/php/JVDB/JVDB2.php';
require_once __DIR__ . '/../../src/php/JVDB/JVConnectionPool.php';
require_once __DIR__ . '/../../src/php/JVDB/JVLogger.php';
require_once __DIR__ . '/../../src/php/JVDB/JVExceptions.php';

use JVDB\JVDB2;
use JVDB\Exceptions\ValidationException;
use JVDB\Exceptions\QueryException;
use JVDB\Exceptions\ConnectionException;
use JVDB\Exceptions\TransactionException;
use JVDB\Exceptions\PoolExhaustedException;
use JVDB\Exceptions\ConfigurationException;

function limpiarPantalla() {
    echo PHP_OS_FAMILY === 'Windows' ? "\033[2J\033[;H" : "\033[2J\033[1;1H";
}

function pausar() {
    echo "\n⏸️  Presiona ENTER para continuar...";
    fgets(STDIN);
}

function ejemploListadoBasico() {
    limpiarPantalla();
    echo str_repeat("=", 80) . "\n";
    echo "📚 EJEMPLO 1: Listado básico de registros\n";
    echo str_repeat("=", 80) . "\n";
    
    $db = new JVDB2(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    
    try {
        // Mostrar estadísticas del pool
        echo "\n🔄 Estado del Pool de Conexiones:\n";
        $stats = $db->getPool() ? $db->getPool()->getStats() : ['total_connections' => 0, 'available' => 0, 'in_use' => 0];
        echo "   Total: {$stats['total_connections']} | Disponibles: {$stats['available']} | En uso: {$stats['in_use']}\n";
        
        // Listar usuarios
        echo "\n👥 USUARIOS:\n";
        echo str_repeat("-", 80) . "\n";
        $usuarios = $db->seleccionar('usuarios', null, null, 'Apellido ASC', 10);
        
        if (count($usuarios) > 0) {
            foreach ($usuarios as $usuario) {
                $estado = $usuario['Activo'] == 1 ? "✅ Activo" : "❌ Inactivo";
                echo "  {$usuario['Nombre']} {$usuario['Apellido']} - {$usuario['Email']} - $estado\n";
            }
            echo "\n📊 Total: " . count($usuarios) . " usuario(s)\n";
        } else {
            echo "  ℹ️  No hay usuarios registrados\n";
        }
        
        // Listar productos
        echo "\n🛍️  PRODUCTOS:\n";
        echo str_repeat("-", 80) . "\n";
        $productos = $db->seleccionar('productos', ['nombre', 'precio', 'stock'], null, null, 5);
        
        if (count($productos) > 0) {
            foreach ($productos as $producto) {
                echo "  {$producto['nombre']} - $" . number_format($producto['precio'], 2) . " (Stock: {$producto['stock']})\n";
            }
            
            // Usar el nuevo método contar()
            $total = $db->contar('productos');
            echo "\n📊 Total: $total producto(s) en la base de datos\n";
        } else {
            echo "  ℹ️  No hay productos registrados\n";
        }
        
    } catch (QueryException $e) {
        echo "\n❌ Error en consulta: " . $e->getMessage() . "\n";
    } finally {
        $db->cerrar();
    }
    
    pausar();
}

function ejemploBusquedaAvanzada() {
    limpiarPantalla();
    echo str_repeat("=", 80) . "\n";
    echo "🔍 EJEMPLO 2: Búsquedas avanzadas con filtros\n";
    echo str_repeat("=", 80) . "\n";
    
    $db = new JVDB2(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    
    try {
        // Búsqueda con WHERE
        echo "\n1️⃣  Buscar usuarios activos:\n";
        echo str_repeat("-", 40) . "\n";
        $activos = $db->seleccionar('usuarios', null, ['Activo' => 1], 'Nombre ASC');
        
        if (count($activos) > 0) {
            foreach ($activos as $usuario) {
                echo "  ✅ {$usuario['Nombre']} {$usuario['Apellido']} - {$usuario['Email']}\n";
            }
            echo "\n📊 " . count($activos) . " usuario(s) activo(s)\n";
        } else {
            echo "  ℹ️  No hay usuarios activos\n";
        }
        
        // Búsqueda con múltiples condiciones
        echo "\n2️⃣  Buscar usuarios mayores de 25 años:\n";
        echo str_repeat("-", 40) . "\n";
        $mayores = $db->consultaPersonalizada(
            "SELECT * FROM usuarios WHERE Edad > ? AND Activo = ? ORDER BY Edad DESC",
            [25, 1],
            "all"
        );
        
        if (count($mayores) > 0) {
            foreach ($mayores as $usuario) {
                echo "  👤 {$usuario['Nombre']} {$usuario['Apellido']} - {$usuario['Edad']} años\n";
            }
        } else {
            echo "  ℹ️  No hay usuarios que cumplan el criterio\n";
        }
        
        // Usar el método existe()
        echo "\n3️⃣  Verificar si existe un email:\n";
        echo str_repeat("-", 40) . "\n";
        echo "  Ingresa un email para buscar: ";
        $emailBuscar = trim(fgets(STDIN));
        
        if (!empty($emailBuscar)) {
            $existe = $db->existe('usuarios', ['Email' => $emailBuscar]);
            if ($existe) {
                echo "  ✅ El email '$emailBuscar' está registrado\n";
            } else {
                echo "  ❌ El email '$emailBuscar' NO está registrado\n";
            }
        }
        
    } catch (QueryException $e) {
        echo "\n❌ Error en consulta: " . $e->getMessage() . "\n";
    } finally {
        $db->cerrar();
    }
    
    pausar();
}

function ejemploInsercion() {
    limpiarPantalla();
    echo str_repeat("=", 80) . "\n";
    echo "➕ EJEMPLO 3: Inserción de registros\n";
    echo str_repeat("=", 80) . "\n";
    
    $db = new JVDB2(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    
    try {
        echo "\n📝 Ingresa los datos del nuevo usuario:\n";
        echo str_repeat("-", 40) . "\n";
        
        echo "  Nombre: ";
        $nombre = trim(fgets(STDIN));
        
        echo "  Apellido: ";
        $apellido = trim(fgets(STDIN));
        
        echo "  Email: ";
        $email = trim(fgets(STDIN));
        
        echo "  Edad: ";
        $edad = trim(fgets(STDIN));
        
        if (empty($nombre) || empty($apellido) || empty($email) || empty($edad)) {
            echo "\n⚠️  Todos los campos son obligatorios\n";
            pausar();
            return;
        }
        
        // Verificar si el email ya existe
        if ($db->existe('usuarios', ['Email' => $email])) {
            echo "\n⚠️  El email '$email' ya está registrado\n";
            pausar();
            return;
        }
        
        // Insertar con return_id
        $nuevoUsuario = [
            'Nombre' => $nombre,
            'Apellido' => $apellido,
            'Email' => $email,
            'Edad' => (int)$edad,
            'Activo' => 1
        ];
        
        echo "\n⏳ Insertando usuario...\n";
        $resultado = $db->insertar('usuarios', $nuevoUsuario, true);
        
        echo "\n✅ Usuario insertado exitosamente\n";
        echo "   ID: " . ($resultado['last_insert_id'] ?? 'N/A') . "\n";
        echo "   Filas afectadas: " . ($resultado['rows_affected'] ?? 0) . "\n";
        
        // Verificar la inserción
        $total = $db->contar('usuarios', ['Activo' => 1]);
        echo "\n📊 Total de usuarios activos: $total\n";
        
    } catch (ValidationException $e) {
        echo "\n❌ Error de validación: " . $e->getMessage() . "\n";
    } catch (QueryException $e) {
        echo "\n❌ Error en inserción: " . $e->getMessage() . "\n";
    } finally {
        $db->cerrar();
    }
    
    pausar();
}

function ejemploInsercionMultiple() {
    limpiarPantalla();
    echo str_repeat("=", 80) . "\n";
    echo "➕➕ EJEMPLO 4: Inserción múltiple (batch insert)\n";
    echo str_repeat("=", 80) . "\n";
    
    $db = new JVDB2(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    
    try {
        echo "\n📝 Insertando 3 usuarios de prueba...\n";
        echo str_repeat("-", 40) . "\n";
        
        $usuariosTest = [
            [
                'Nombre' => 'Test1',
                'Apellido' => 'Usuario1',
                'Email' => 'test1_' . bin2hex(random_bytes(4)) . '@test.com',
                'Edad' => 25,
                'Activo' => 1
            ],
            [
                'Nombre' => 'Test2',
                'Apellido' => 'Usuario2',
                'Email' => 'test2_' . bin2hex(random_bytes(4)) . '@test.com',
                'Edad' => 30,
                'Activo' => 1
            ],
            [
                'Nombre' => 'Test3',
                'Apellido' => 'Usuario3',
                'Email' => 'test3_' . bin2hex(random_bytes(4)) . '@test.com',
                'Edad' => 35,
                'Activo' => 1
            ]
        ];
        
        // Inserción múltiple con transacción automática
        $filasInsertadas = $db->insertarMultiple('usuarios', $usuariosTest);
        
        echo "\n✅ $filasInsertadas usuario(s) insertado(s) exitosamente\n";
        echo "   ℹ️  La transacción se realizó automáticamente\n";
        
        // Mostrar los usuarios insertados
        echo "\n👥 Usuarios de prueba insertados:\n";
        foreach ($usuariosTest as $usuario) {
            echo "   - {$usuario['Nombre']} {$usuario['Apellido']} ({$usuario['Email']})\n";
        }
        
        // Preguntar si desea eliminarlos
        echo "\n" . str_repeat("-", 40) . "\n";
        echo "¿Deseas eliminar estos usuarios de prueba? (s/n): ";
        $eliminar = trim(fgets(STDIN));
        
        if (strtolower($eliminar) === 's') {
            echo "\n⏳ Eliminando usuarios de prueba...\n";
            foreach ($usuariosTest as $usuario) {
                $db->eliminar('usuarios', ['Email' => $usuario['Email']]);
            }
            echo "✅ Usuarios de prueba eliminados\n";
        }
        
    } catch (QueryException $e) {
        echo "\n❌ Error en inserción múltiple: " . $e->getMessage() . "\n";
    } finally {
        $db->cerrar();
    }
    
    pausar();
}

function ejemploActualizacion() {
    limpiarPantalla();
    echo str_repeat("=", 80) . "\n";
    echo "✏️  EJEMPLO 5: Actualización de registros\n";
    echo str_repeat("=", 80) . "\n";
    
    $db = new JVDB2(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    
    try {
        // Listar usuarios actuales
        echo "\n👥 Usuarios actuales:\n";
        echo str_repeat("-", 40) . "\n";
        $usuarios = $db->seleccionar('usuarios', null, null, null, 10);
        
        if (count($usuarios) === 0) {
            echo "  ℹ️  No hay usuarios para actualizar\n";
            pausar();
            return;
        }
        
        $i = 1;
        foreach ($usuarios as $usuario) {
            $estado = $usuario['Activo'] == 1 ? "✅" : "❌";
            echo "  $i. {$usuario['Nombre']} {$usuario['Apellido']} - {$usuario['Email']} $estado\n";
            $i++;
        }
        
        // Seleccionar usuario
        echo "\n" . str_repeat("-", 40) . "\n";
        echo "Selecciona el número de usuario a actualizar (0 para cancelar): ";
        $seleccion = trim(fgets(STDIN));
        
        if (!is_numeric($seleccion) || $seleccion < 1 || $seleccion > count($usuarios)) {
            echo "\n⚠️  Selección inválida\n";
            pausar();
            return;
        }
        
        $usuarioSeleccionado = $usuarios[$seleccion - 1];
        
        echo "\n📝 Actualizando: {$usuarioSeleccionado['Nombre']} {$usuarioSeleccionado['Apellido']}\n";
        echo str_repeat("-", 40) . "\n";
        
        echo "\n¿Qué deseas actualizar?\n";
        echo "  1. Cambiar estado (Activo/Inactivo)\n";
        echo "  2. Cambiar edad\n";
        echo "  3. Cambiar email\n";
        
        echo "\n👉 Opción: ";
        $opcion = trim(fgets(STDIN));
        
        if ($opcion === '1') {
            $nuevoEstado = $usuarioSeleccionado['Activo'] == 1 ? 0 : 1;
            $filas = $db->actualizar(
                'usuarios',
                ['Activo' => $nuevoEstado],
                ['Email' => $usuarioSeleccionado['Email']]
            );
            $estadoTexto = $nuevoEstado == 1 ? "Activo" : "Inactivo";
            echo "\n✅ Usuario actualizado a: $estadoTexto\n";
            echo "   Filas afectadas: $filas\n";
            
        } elseif ($opcion === '2') {
            echo "  Nueva edad: ";
            $nuevaEdad = trim(fgets(STDIN));
            if (is_numeric($nuevaEdad)) {
                $filas = $db->actualizar(
                    'usuarios',
                    ['Edad' => (int)$nuevaEdad],
                    ['Email' => $usuarioSeleccionado['Email']]
                );
                echo "\n✅ Edad actualizada a: $nuevaEdad\n";
                echo "   Filas afectadas: $filas\n";
            } else {
                echo "\n❌ Edad inválida\n";
            }
            
        } elseif ($opcion === '3') {
            echo "  Nuevo email: ";
            $nuevoEmail = trim(fgets(STDIN));
            if (!empty($nuevoEmail) && strpos($nuevoEmail, '@') !== false) {
                // Verificar si el nuevo email ya existe
                if ($db->existe('usuarios', ['Email' => $nuevoEmail])) {
                    echo "\n⚠️  El email '$nuevoEmail' ya está registrado\n";
                } else {
                    $filas = $db->actualizar(
                        'usuarios',
                        ['Email' => $nuevoEmail],
                        ['Email' => $usuarioSeleccionado['Email']]
                    );
                    echo "\n✅ Email actualizado\n";
                    echo "   Filas afectadas: $filas\n";
                }
            } else {
                echo "\n❌ Email inválido\n";
            }
        } else {
            echo "\n⚠️  Opción inválida\n";
        }
        
    } catch (ValidationException $e) {
        echo "\n❌ Error de validación: " . $e->getMessage() . "\n";
    } catch (QueryException $e) {
        echo "\n❌ Error en actualización: " . $e->getMessage() . "\n";
    } finally {
        $db->cerrar();
    }
    
    pausar();
}

function ejemploEliminacion() {
    limpiarPantalla();
    echo str_repeat("=", 80) . "\n";
    echo "🗑️  EJEMPLO 6: Eliminación de registros\n";
    echo str_repeat("=", 80) . "\n";
    
    $db = new JVDB2(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    
    try {
        // Buscar usuarios de prueba
        echo "\n🔍 Buscando usuarios de prueba (emails con 'test')...\n";
        echo str_repeat("-", 40) . "\n";
        
        $usuariosTest = $db->consultaPersonalizada(
            "SELECT * FROM usuarios WHERE Email LIKE ?",
            ['%test%'],
            "all"
        );
        
        if (count($usuariosTest) === 0) {
            echo "  ℹ️  No hay usuarios de prueba para eliminar\n";
            echo "\n💡 Puedes crear usuarios de prueba con el Ejemplo 4\n";
            pausar();
            return;
        }
        
        echo "\n👥 Encontrados " . count($usuariosTest) . " usuario(s) de prueba:\n";
        foreach ($usuariosTest as $usuario) {
            echo "   - {$usuario['Nombre']} {$usuario['Apellido']} ({$usuario['Email']})\n";
        }
        
        echo "\n" . str_repeat("-", 40) . "\n";
        echo "¿Deseas eliminar TODOS estos usuarios? (s/n): ";
        $confirmar = trim(fgets(STDIN));
        
        if (strtolower($confirmar) === 's') {
            echo "\n⏳ Eliminando usuarios...\n";
            $totalEliminados = 0;
            
            foreach ($usuariosTest as $usuario) {
                $filas = $db->eliminar('usuarios', ['Email' => $usuario['Email']]);
                $totalEliminados += $filas ?: 0;
            }
            
            echo "\n✅ $totalEliminados usuario(s) eliminado(s) exitosamente\n";
            
            // Verificar
            $restantes = $db->contar('usuarios');
            echo "📊 Usuarios restantes en la base de datos: $restantes\n";
        } else {
            echo "\n⏸️  Operación cancelada\n";
        }
        
    } catch (QueryException $e) {
        echo "\n❌ Error en eliminación: " . $e->getMessage() . "\n";
    } finally {
        $db->cerrar();
    }
    
    pausar();
}

function ejemploTransacciones() {
    limpiarPantalla();
    echo str_repeat("=", 80) . "\n";
    echo "🔄 EJEMPLO 7: Transacciones con rollback\n";
    echo str_repeat("=", 80) . "\n";
    
    $db = new JVDB2(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    
    try {
        echo "\n📝 Demostración de transacción con rollback\n";
        echo str_repeat("-", 40) . "\n";
        
        // Contar usuarios actuales
        $usuariosAntes = $db->contar('usuarios');
        echo "\n🔢 Usuarios antes de la transacción: $usuariosAntes\n";
        
        echo "\n⏳ Iniciando transacción...\n";
        echo "   1. Insertando usuario temporal\n";
        echo "   2. Realizando rollback\n";
        
        // Iniciar transacción
        $db->beginTransaction();
        
        try {
            // Insertar un usuario
            $usuarioTemporal = [
                'Nombre' => 'Temporal',
                'Apellido' => 'Rollback',
                'Email' => 'temporal@rollback.com',
                'Edad' => 99,
                'Activo' => 1
            ];
            $db->insertar('usuarios', $usuarioTemporal);
            echo "\n   ✅ Usuario temporal insertado\n";
            
            // Verificar que existe (dentro de la transacción)
            $usuariosDurante = $db->contar('usuarios');
            echo "   🔢 Usuarios durante la transacción: $usuariosDurante\n";
            
            // Hacer rollback
            echo "\n   🔄 Ejecutando rollback...\n";
            $db->rollback();
            
        } catch (Exception $e) {
            echo "   ❌ Error: " . $e->getMessage() . "\n";
            $db->rollback();
        }
        
        // Verificar después del rollback
        $usuariosDespues = $db->contar('usuarios');
        echo "\n🔢 Usuarios después del rollback: $usuariosDespues\n";
        
        if ($usuariosAntes == $usuariosDespues) {
            echo "\n✅ ¡Rollback exitoso! Los datos no fueron modificados\n";
        } else {
            echo "\n⚠️  Advertencia: Hubo cambios inesperados\n";
        }
        
    } catch (Exception $e) {
        echo "\n❌ Error: " . $e->getMessage() . "\n";
    } finally {
        $db->cerrar();
    }
    
    pausar();
}

function ejemploEstadisticas() {
    limpiarPantalla();
    echo str_repeat("=", 80) . "\n";
    echo "📊 EJEMPLO 8: Estadísticas y agregaciones\n";
    echo str_repeat("=", 80) . "\n";
    
    $db = new JVDB2(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    
    try {
        // Estadísticas del pool
        echo "\n🔄 ESTADO DEL POOL DE CONEXIONES:\n";
        echo str_repeat("-", 40) . "\n";
        if ($db->getPool()) {
            $stats = $db->getPool()->getStats();
            echo "  Total de conexiones: {$stats['total_connections']}\n";
            echo "  Conexiones disponibles: {$stats['available']}\n";
            echo "  Conexiones en uso: {$stats['in_use']}\n";
        } else {
            echo "  ℹ️  Pool no configurado (conexión directa)\n";
        }
        
        // Estadísticas de usuarios
        echo "\n👥 ESTADÍSTICAS DE USUARIOS:\n";
        echo str_repeat("-", 40) . "\n";
        
        $totalUsuarios = $db->contar('usuarios');
        $usuariosActivos = $db->contar('usuarios', ['Activo' => 1]);
        $usuariosInactivos = $totalUsuarios - $usuariosActivos;
        
        echo "  Total de usuarios: $totalUsuarios\n";
        if ($totalUsuarios > 0) {
            $pctActivos = ($usuariosActivos / $totalUsuarios) * 100;
            $pctInactivos = ($usuariosInactivos / $totalUsuarios) * 100;
            echo "  Usuarios activos: $usuariosActivos (" . number_format($pctActivos, 1) . "%)\n";
            echo "  Usuarios inactivos: $usuariosInactivos (" . number_format($pctInactivos, 1) . "%)\n";
        }
        
        // Edad promedio
        $resultado = $db->consultaPersonalizada(
            "SELECT AVG(Edad) as edad_promedio, MIN(Edad) as edad_min, MAX(Edad) as edad_max FROM usuarios WHERE Edad IS NOT NULL",
            [],
            "one"
        );
        
        if ($resultado && $resultado['edad_promedio']) {
            echo "\n📈 ANÁLISIS DE EDADES:\n";
            echo str_repeat("-", 40) . "\n";
            echo "  Edad promedio: " . number_format($resultado['edad_promedio'], 1) . " años\n";
            echo "  Edad mínima: {$resultado['edad_min']} años\n";
            echo "  Edad máxima: {$resultado['edad_max']} años\n";
        }
        
        // Usuarios por estado
        echo "\n📋 DISTRIBUCIÓN POR ESTADO:\n";
        echo str_repeat("-", 40) . "\n";
        $resultado = $db->consultaPersonalizada(
            "SELECT Activo, COUNT(*) as total FROM usuarios GROUP BY Activo",
            [],
            "all"
        );
        
        if ($resultado) {
            foreach ($resultado as $fila) {
                $estado = $fila['Activo'] == 1 ? "Activos" : "Inactivos";
                echo "  $estado: {$fila['total']}\n";
            }
        }
        
    } catch (QueryException $e) {
        echo "\n❌ Error en consulta: " . $e->getMessage() . "\n";
    } finally {
        $db->cerrar();
    }
    
    pausar();
}

function verLogs() {
    limpiarPantalla();
    echo str_repeat("=", 80) . "\n";
    echo "📋 LOGS DEL SISTEMA\n";
    echo str_repeat("=", 80) . "\n";
    
    $logFile = __DIR__ . '/../../logs/jvdb.log';
    
    if (file_exists($logFile)) {
        echo "\n📁 Archivo: $logFile\n";
        echo str_repeat("-", 80) . "\n";
        
        $lines = file($logFile);
        $ultimasLineas = array_slice($lines, -30);
        
        echo "\n🔍 Últimas 30 líneas del log:\n\n";
        foreach ($ultimasLineas as $line) {
            echo rtrim($line) . "\n";
        }
    } else {
        echo "\n⚠️  No se encontró el archivo de log\n";
        echo "   Ejecuta algunos ejemplos primero para generar logs\n";
    }
    
    pausar();
}

function menuPrincipal() {
    while (true) {
        limpiarPantalla();
        echo "\n" . str_repeat("=", 80) . "\n";
        echo "🚀 JVDataAccess v2.0 - Menú Interactivo (PHP)\n";
        echo str_repeat("=", 80) . "\n";
        echo "\n📚 EJEMPLOS CRUD BÁSICOS:\n";
        echo "  1.  Listado básico de registros\n";
        echo "  2.  Búsquedas avanzadas con filtros\n";
        echo "  3.  Inserción de un registro\n";
        echo "  4.  Inserción múltiple (batch)\n";
        echo "  5.  Actualización de registros\n";
        echo "  6.  Eliminación de registros\n";
        
        echo "\n⚙️  FUNCIONALIDADES AVANZADAS:\n";
        echo "  7.  Demostración de transacciones\n";
        echo "  8.  Estadísticas y agregaciones\n";
        
        echo "\n🔧 UTILIDADES:\n";
        echo "  9.  Ver logs del sistema\n";
        
        echo "\n  0.  Salir\n";
        echo str_repeat("-", 80) . "\n";
        
        echo "\n👉 Selecciona una opción: ";
        $opcion = trim(fgets(STDIN));
        
        switch ($opcion) {
            case '1':
                ejemploListadoBasico();
                break;
            case '2':
                ejemploBusquedaAvanzada();
                break;
            case '3':
                ejemploInsercion();
                break;
            case '4':
                ejemploInsercionMultiple();
                break;
            case '5':
                ejemploActualizacion();
                break;
            case '6':
                ejemploEliminacion();
                break;
            case '7':
                ejemploTransacciones();
                break;
            case '8':
                ejemploEstadisticas();
                break;
            case '9':
                verLogs();
                break;
            case '0':
                limpiarPantalla();
                echo "\n" . str_repeat("=", 80) . "\n";
                echo "👋 ¡Gracias por usar JVDataAccess v2.0!\n";
                echo str_repeat("=", 80) . "\n";
                echo "\n📚 Recursos:\n";
                echo "  - Documentación: docs/GUIA_V2.md\n";
                echo "  - Logs: logs/jvdb.log\n";
                echo "\n";
                exit(0);
            default:
                echo "\n❌ Opción no válida\n";
                pausar();
        }
    }
}

// Punto de entrada
limpiarPantalla();
echo "\n" . str_repeat("=", 80) . "\n";
echo "🚀 JVDataAccess v2.0 - Sistema de Gestión de Base de Datos (PHP)\n";
echo str_repeat("=", 80) . "\n";
echo "\n✨ Características:\n";
echo "  ✅ Pool de conexiones para mejor rendimiento\n";
echo "  ✅ Sistema de logging avanzado\n";
echo "  ✅ Transacciones con rollback\n";
echo "  ✅ Excepciones personalizadas\n";
echo "  ✅ Métodos CRUD optimizados\n";

echo "\n⚠️  REQUISITOS:\n";
echo "  1. Base de datos configurada (ejecuta: php crear_tabla_usuarios.php)\n";
echo "  2. Credenciales en config.php actualizadas\n";
echo "  3. Tabla 'usuarios' creada\n";

echo "\n" . str_repeat("-", 80) . "\n";
echo "\n¿Continuar? (s/n): ";
$respuesta = trim(fgets(STDIN));

if (strtolower($respuesta) === 's') {
    menuPrincipal();
} else {
    echo "\n👋 ¡Hasta luego!\n\n";
}
