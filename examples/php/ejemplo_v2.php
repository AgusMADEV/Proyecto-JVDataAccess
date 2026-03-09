<?php
/**
 * Ejemplo de uso de JVDB 2.0 - Versión avanzada con pool de conexiones (PHP)
 * Versión: 2.0.0
 * 
 * Demuestra las nuevas características de JVDB2:
 * - Pool de conexiones
 * - Sistema de logging
 * - Transacciones
 * - CRUD optimizado
 * - Manejo robusto de errores
 */

require_once __DIR__ . '/../../config.php';
require_once __DIR__ . '/../../src/php/JVDB/JVDB2.php';

use JVDB\JVDB2;
use JVDB\Exceptions\ValidationException;
use JVDB\Exceptions\QueryException;
use JVDB\Exceptions\ConnectionException;
use JVDB\Exceptions\TransactionException;
use JVDB\Exceptions\PoolExhaustedException;
use JVDB\Exceptions\ConfigurationException;


function ejemploBasico() {
    echo str_repeat("=", 60) . "\n";
    echo "EJEMPLO 1: Uso básico con pool de conexiones\n";
    echo str_repeat("=", 60) . "\n";
    
    // Configuración del pool
    $poolConfig = [
        'min_size' => 2,
        'max_size' => 5,
        'max_lifetime' => 3600,
        'timeout' => 10
    ];
    
    // Configuración del logger
    $logConfig = [
        'log_dir' => 'logs',
        'console_output' => true,
        'file_output' => true
    ];
    
    // Crear instancia de JVDB2
    $db = new JVDB2(
        DB_HOST,
        DB_USER,
        DB_PASSWORD,
        DB_NAME,
        DB_PORT,
        true,  // use_pool
        $poolConfig,
        $logConfig
    );
    
    try {
        // Consulta simple
        $usuarios = $db->seleccionar('usuarios');
        echo "\nUsuarios encontrados: " . count($usuarios) . "\n";
        foreach (array_slice($usuarios, 0, 3) as $usuario) {
            echo "  - {$usuario['Nombre']} {$usuario['Apellido']}\n";
        }
        
        // Estadísticas del pool
        $stats = $db->getPoolStats();
        echo "\nEstadísticas del pool:\n";
        echo "  Total conexiones: {$stats['total_connections']}\n";
        echo "  En uso: {$stats['in_use']}\n";
        echo "  Disponibles: {$stats['available']}\n";
        
    } finally {
        $db->cerrar();
    }
}


function ejemploCrudAvanzado() {
    echo "\n" . str_repeat("=", 60) . "\n";
    echo "EJEMPLO 2: CRUD avanzado\n";
    echo str_repeat("=", 60) . "\n";
    
    $db = new JVDB2(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT, true);
    
    try {
        // SELECT con WHERE, ORDER BY y LIMIT
        echo "\n1. SELECT avanzado:\n";
        $usuarios = $db->seleccionar(
            'usuarios',
            ['Nombre', 'Apellido', 'Email'],
            ['Activo' => 1],
            'Apellido ASC',
            5
        );
        echo "   " . count($usuarios) . " usuarios activos\n";
        
        // INSERT con return_id
        echo "\n2. INSERT con ID retornado:\n";
        $nuevoUsuario = [
            'Nombre' => 'Ana',
            'Apellido' => 'García',
            'Email' => 'ana.garcia@example.com',
            'Edad' => 28,
            'Activo' => 1
        ];
        $resultado = $db->insertar('usuarios', $nuevoUsuario, true);
        echo "   Insertado ID: {$resultado['last_insert_id']}\n";
        
        // UPDATE con WHERE personalizado
        echo "\n3. UPDATE con condiciones:\n";
        $filas = $db->actualizar(
            'usuarios',
            ['Activo' => 0],
            null,
            ['Email' => 'ana.garcia@example.com']
        );
        echo "   $filas fila(s) actualizada(s)\n";
        
        // COUNT
        echo "\n4. COUNT:\n";
        $total = $db->contar('usuarios');
        $activos = $db->contar('usuarios', ['Activo' => 1]);
        echo "   Total usuarios: $total\n";
        echo "   Usuarios activos: $activos\n";
        
        // EXISTS
        echo "\n5. EXISTS:\n";
        $existe = $db->existe('usuarios', ['Email' => 'ana.garcia@example.com']);
        echo "   ¿Existe el email?: " . ($existe ? 'Sí' : 'No') . "\n";
        
        // DELETE
        echo "\n6. DELETE:\n";
        $eliminados = $db->eliminar('usuarios', null, ['Email' => 'ana.garcia@example.com']);
        echo "   $eliminados registro(s) eliminado(s)\n";
        
    } finally {
        $db->cerrar();
    }
}


function ejemploTransacciones() {
    echo "\n" . str_repeat("=", 60) . "\n";
    echo "EJEMPLO 3: Transacciones\n";
    echo str_repeat("=", 60) . "\n";
    
    $db = new JVDB2(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT, true);
    
    try {
        echo "\nInsertando múltiples registros en transacción...\n";
        
        $db->beginTransaction();
        
        try {
            // Insertar varios usuarios
            $usuarios = [
                ['Nombre' => 'Carlos', 'Apellido' => 'López', 'Email' => 'carlos@test.com', 'Edad' => 35, 'Activo' => 1],
                ['Nombre' => 'María', 'Apellido' => 'Ruiz', 'Email' => 'maria@test.com', 'Edad' => 29, 'Activo' => 1],
                ['Nombre' => 'Pedro', 'Apellido' => 'Sanz', 'Email' => 'pedro@test.com', 'Edad' => 42, 'Activo' => 1]
            ];
            
            foreach ($usuarios as $usuario) {
                $db->insertar('usuarios', $usuario);
            }
            
            $db->commit();
            echo "✅ Transacción completada exitosamente\n";
            
        } catch (Exception $e) {
            $db->rollback();
            throw $e;
        }
        
        // Verificar
        $total = $db->contar('usuarios', ['Activo' => 1]);
        echo "Total usuarios activos: $total\n";
        
        // Ejemplo de rollback
        echo "\nProbando rollback...\n";
        try {
            $db->beginTransaction();
            $db->insertar('usuarios', ['Nombre' => 'Test', 'Apellido' => 'User', 'Email' => 'test@test.com', 'Edad' => 25, 'Activo' => 1]);
            // Simular un error
            throw new Exception("Error simulado");
        } catch (Exception $e) {
            $db->rollback();
            echo "⚠️  Transacción revertida: {$e->getMessage()}\n";
        }
        
        // Limpiar datos de prueba
        echo "\nLimpiando datos de prueba...\n";
        $db->eliminar('usuarios', null, ['Email' => 'carlos@test.com']);
        $db->eliminar('usuarios', null, ['Email' => 'maria@test.com']);
        $db->eliminar('usuarios', null, ['Email' => 'pedro@test.com']);
        
    } finally {
        $db->cerrar();
    }
}


function ejemploInsercionMultiple() {
    echo "\n" . str_repeat("=", 60) . "\n";
    echo "EJEMPLO 4: Inserción múltiple\n";
    echo str_repeat("=", 60) . "\n";
    
    $db = new JVDB2(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT, true);
    
    try {
        // Crear múltiples registros
        $usuarios = [];
        for ($i = 0; $i < 5; $i++) {
            $usuarios[] = [
                'Nombre' => "Usuario$i",
                'Apellido' => "Apellido$i",
                'Email' => "usuario$i@test.com",
                'Edad' => 20 + $i,
                'Activo' => 1
            ];
        }
        
        echo "\nInsertando " . count($usuarios) . " usuarios...\n";
        $total = $db->insertarMultiple('usuarios', $usuarios);
        echo "✅ $total registros insertados\n";
        
        // Limpiar
        echo "\nLimpiando registros de prueba...\n";
        for ($i = 0; $i < 5; $i++) {
            $db->eliminar('usuarios', null, ['Email' => "usuario$i@test.com"]);
        }
        
    } finally {
        $db->cerrar();
    }
}


function ejemploManejoErrores() {
    echo "\n" . str_repeat("=", 60) . "\n";
    echo "EJEMPLO 5: Manejo de errores\n";
    echo str_repeat("=", 60) . "\n";
    
    $db = new JVDB2(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT, true);
    
    try {
        // Intentar insertar sin datos
        echo "\n1. Intentando insertar sin datos:\n";
        try {
            $db->insertar('usuarios', []);
        } catch (ValidationException $e) {
            echo "   ✅ ValidationException capturado: {$e->getMessage()}\n";
        }
        
        // Intentar actualizar sin condiciones
        echo "\n2. Intentando actualizar sin condiciones:\n";
        try {
            $db->actualizar('usuarios', ['Nombre' => 'Test']);
        } catch (ValidationException $e) {
            echo "   ✅ ValidationException capturado: {$e->getMessage()}\n";
        }
        
        // Consulta con tabla inexistente
        echo "\n3. Intentando consultar tabla inexistente:\n";
        try {
            $db->seleccionar('tabla_que_no_existe');
        } catch (QueryException $e) {
            echo "   ✅ QueryException capturado\n";
        }
        
    } finally {
        $db->cerrar();
    }
}


function ejemploConsultasPersonalizadas() {
    echo "\n" . str_repeat("=", 60) . "\n";
    echo "EJEMPLO 6: Consultas personalizadas\n";
    echo str_repeat("=", 60) . "\n";
    
    $db = new JVDB2(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT, true);
    
    try {
        // Consulta con agregación
        echo "\n1. Consulta con agregación:\n";
        $resultado = $db->consultaPersonalizada(
            "SELECT Activo, COUNT(*) as total FROM usuarios GROUP BY Activo"
        );
        echo "   Usuarios por estado:\n";
        foreach ($resultado as $row) {
            $estado = $row['Activo'] == 1 ? "Activos" : "Inactivos";
            echo "   - $estado: {$row['total']}\n";
        }
        
        // Consulta con parámetros
        echo "\n2. Consulta con parámetros:\n";
        $resultado = $db->consultaPersonalizada(
            "SELECT * FROM usuarios WHERE Edad > ? AND Activo = ? LIMIT 5",
            [25, 1]
        );
        echo "   " . count($resultado) . " usuarios mayores de 25 años\n";
        
    } finally {
        $db->cerrar();
    }
}


// Ejecutar ejemplos
echo "\n" . str_repeat("=", 60) . "\n";
echo "DEMOSTRACIONES DE JVDB 2.0 (PHP)\n";
echo str_repeat("=", 60) . "\n";

try {
    ejemploBasico();
    ejemploCrudAvanzado();
    ejemploTransacciones();
    ejemploInsercionMultiple();
    ejemploManejoErrores();
    ejemploConsultasPersonalizadas();
    
    echo "\n" . str_repeat("=", 60) . "\n";
    echo "✅ Todos los ejemplos completados\n";
    echo str_repeat("=", 60) . "\n";
    
} catch (Exception $e) {
    echo "\n❌ Error en los ejemplos: {$e->getMessage()}\n";
    echo $e->getTraceAsString() . "\n";
}
