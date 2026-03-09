<?php
/**
 * Ejemplo básico de uso de JVDataAccess en PHP
 * Versión: 1.0.0
 * 
 * Este ejemplo demuestra las funcionalidades básicas de:
 * - YourSQL: Conector MySQL personalizado
 * - JVDB: Clase de abstracción para base de datos
 */

// Cargar configuración
require_once __DIR__ . '/../../config.php';

// Cargar clases
require_once __DIR__ . '/../../src/php/JVDB/JVDB.php';

use JVDB\JVDB;

function imprimirSeparador($titulo) {
    echo "\n" . str_repeat("=", 80) . "\n";
    echo "📚 $titulo\n";
    echo str_repeat("=", 80) . "\n";
}

function imprimirSubtitulo($numero, $titulo) {
    echo "\n$numero  $titulo:\n";
    echo str_repeat("-", 60) . "\n";
}

/**
 * Ejemplo básico de uso de JVDB
 */
function ejemploJVDBBasico() {
    imprimirSeparador("EJEMPLO 1: Uso básico de JVDB");
    
    // Crear instancia de JVDB (sin echo de conexión para este ejemplo)
    ob_start();
    $db = new JVDB(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);
    ob_end_clean();
    
    // 1. Listar todas las tablas
    imprimirSubtitulo("1️⃣", "Listar tablas de la base de datos");
    $tablas = $db->tablas('array');
    foreach ($tablas as $tabla) {
        echo "  📋 $tabla\n";
    }
    
    // 2. Consultar productos
    imprimirSubtitulo("2️⃣", "Consultar todos los productos");
    $productos = $db->seleccionar('productos', '*', 'array');
    foreach (array_slice($productos, 0, 3) as $producto) {
        echo "  🛍️  {$producto['nombre']} - \${$producto['precio']}\n";
    }
    
    // 3. Buscar productos por categoría
    imprimirSubtitulo("3️⃣", "Buscar productos de categoría 'Periféricos'");
    $perifericos = $db->buscar('productos', 'categoria', 'Periféricos', 'array');
    foreach ($perifericos as $producto) {
        echo "  ⌨️  {$producto['nombre']} - Stock: {$producto['stock']}\n";
    }
    
    // 4. Insertar un nuevo producto
    imprimirSubtitulo("4️⃣", "Insertar nuevo producto");
    $nuevoProducto = [
        'nombre' => 'Micrófono Blue Yeti',
        'descripcion' => 'Micrófono USB profesional',
        'precio' => 129.99,
        'stock' => 15,
        'categoria' => 'Audio'
    ];
    $db->insertar('productos', $nuevoProducto);
    
    // 5. Consultar un registro específico
    imprimirSubtitulo("5️⃣", "Consultar cliente por ID");
    $cliente = $db->seleccionarUno('clientes', 1);
    if ($cliente) {
        echo "  👤 {$cliente['nombre']} {$cliente['apellidos']}\n";
        echo "  📧 {$cliente['email']}\n";
    }
    
    // Cerrar conexión
    unset($db);
    echo "\n✅ Ejemplo completado con éxito\n";
}

/**
 * Ejemplo de consultas más avanzadas con JVDB
 */
function ejemploConsultasAvanzadas() {
    imprimirSeparador("EJEMPLO 2: Consultas avanzadas con JVDB");
    
    ob_start();
    $db = new JVDB(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);
    ob_end_clean();
    
    // 1. Consulta personalizada con JOIN
    imprimirSubtitulo("1️⃣", "Consulta con JOIN - Pedidos con datos de clientes");
    $query = "
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
    ";
    $pedidos = $db->consultaPersonalizada($query, null, 'array');
    foreach ($pedidos as $pedido) {
        echo "  📦 Pedido #{$pedido['Identificador']} - {$pedido['nombre']}\n";
        echo "     Estado: {$pedido['estado']} | Total: \${$pedido['total']}\n";
    }
    
    // 2. Actualizar un producto
    imprimirSubtitulo("2️⃣", "Actualizar stock de un producto");
    $db->actualizar('productos', 2, ['stock' => 60]);
    $producto = $db->seleccionarUno('productos', 2);
    echo "  Stock actualizado: {$producto['nombre']} -> {$producto['stock']} unidades\n";
    
    // 3. Estructura de una tabla
    imprimirSubtitulo("3️⃣", "Ver estructura de tabla 'productos'");
    $estructura = $db->estructuraTabla('productos', 'array');
    foreach ($estructura as $columna) {
        echo "  🔹 {$columna['Field']} - {$columna['Type']}\n";
    }
    
    // 4. Uso de transacciones
    imprimirSubtitulo("4️⃣", "Ejemplo de transacción");
    try {
        $db->iniciarTransaccion();
        
        // Insertar un nuevo cliente
        $nuevoCliente = [
            'nombre' => 'Luis',
            'apellidos' => 'González Martín',
            'email' => 'luis.gonzalez@email.com',
            'telefono' => '600678901',
            'ciudad' => 'Sevilla'
        ];
        $db->insertar('clientes', $nuevoCliente);
        
        // Confirmar transacción
        $db->confirmarTransaccion();
        
    } catch (Exception $e) {
        echo "  ❌ Error: " . $e->getMessage() . "\n";
        $db->revertirTransaccion();
    }
    
    unset($db);
    echo "\n✅ Ejemplo completado con éxito\n";
}

/**
 * Ejemplo de uso directo de YourSQL
 */
function ejemploYourSQLDirecto() {
    imprimirSeparador("EJEMPLO 3: Uso directo de YourSQL (bajo nivel)");
    
    require_once __DIR__ . '/../../src/php/YourSQL/YourSQL.php';
    
    // Crear conexión con YourSQL (usando namespace completo)
    $conexion = new \YourSQL\YourSQLConnection(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);
    $conexion->connect();
    echo "\n✅ Conexión establecida con YourSQL\n";
    
    // 1. Query directo
    imprimirSubtitulo("1️⃣", "Consulta directa con YourSQL");
    $resultado = $conexion->executeQuery("SELECT * FROM productos WHERE precio < 100");
    foreach ($resultado as $producto) {
        echo "  💰 {$producto['nombre']} - \${$producto['precio']}\n";
    }
    
    // 2. Query con parámetros (prepared statement)
    imprimirSubtitulo("2️⃣", "Consulta preparada con parámetros");
    $resultado = $conexion->executeQuery(
        "SELECT * FROM productos WHERE categoria = ?",
        ['Audio']
    );
    foreach ($resultado as $producto) {
        echo "  🎧 {$producto['nombre']}\n";
    }
    
    // 3. Query Builder
    imprimirSubtitulo("3️⃣", "Uso del Query Builder");
    $builder = new \YourSQL\YourSQLQueryBuilder($conexion);
    $resultado = $builder
        ->select('nombre', 'email', 'ciudad')
        ->from('clientes')
        ->where("ciudad = 'Barcelona'")
        ->orderBy('nombre', 'ASC')
        ->execute();
    
    foreach ($resultado as $cliente) {
        echo "  🌆 {$cliente['nombre']} - {$cliente['ciudad']}\n";
    }
    
    // 4. Información de tablas
    imprimirSubtitulo("4️⃣", "Listar todas las tablas");
    $tablas = $conexion->getTables();
    foreach ($tablas as $tabla) {
        echo "  📋 $tabla\n";
    }
    
    $conexion->disconnect();
    echo "\n✅ Ejemplo completado con éxito\n";
}

/**
 * Menú interactivo
 */
function menuPrincipal() {
    while (true) {
        echo "\n" . str_repeat("=", 80) . "\n";
        echo "🚀 JVDataAccess - Ejemplos de Uso (PHP)\n";
        echo str_repeat("=", 80) . "\n";
        echo "\nSelecciona un ejemplo:\n";
        echo "  1. Uso básico de JVDB\n";
        echo "  2. Consultas avanzadas\n";
        echo "  3. Uso directo de YourSQL\n";
        echo "  4. Ejecutar todos los ejemplos\n";
        echo "  0. Salir\n";
        echo str_repeat("-", 80) . "\n";
        
        echo "\n👉 Opción: ";
        $opcion = trim(fgets(STDIN));
        
        switch ($opcion) {
            case '1':
                ejemploJVDBBasico();
                break;
            case '2':
                ejemploConsultasAvanzadas();
                break;
            case '3':
                ejemploYourSQLDirecto();
                break;
            case '4':
                ejemploJVDBBasico();
                ejemploConsultasAvanzadas();
                ejemploYourSQLDirecto();
                break;
            case '0':
                echo "\n👋 ¡Hasta luego!\n\n";
                exit(0);
            default:
                echo "\n❌ Opción no válida\n";
        }
        
        echo "\nPresiona ENTER para continuar...";
        fgets(STDIN);
    }
}

// Punto de entrada
echo "\n⚠️  Asegúrate de haber ejecutado el script database/init.sql primero\n";
echo "    y de configurar tus credenciales en config.php\n\n";
echo "¿Continuar? (s/n): ";
$respuesta = trim(fgets(STDIN));

if (strtolower($respuesta) === 's') {
    menuPrincipal();
} else {
    echo "\n👋 ¡Hasta luego!\n\n";
}
