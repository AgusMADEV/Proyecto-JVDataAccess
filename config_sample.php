<?php
/**
 * Configuración de la base de datos
 * Versión: 1.0.0
 * 
 * Define aquí tus credenciales de base de datos
 */

// Configuración de MySQL
define('DB_HOST', 'localhost');
define('DB_USER', 'tu_usuario');          // Cambia esto por tu usuario
define('DB_PASSWORD', 'tu_contraseña');          // Cambia esto por tu contraseña
define('DB_NAME', 'jvdataaccess_demo');
define('DB_PORT', 3306);

// Configuración alternativa para desarrollo
const DB_CONFIG_DEV = [
    'host' => 'localhost',
    'user' => 'tu_usuario',
    'password' => 'tu_contraseña',
    'database' => 'jvdataaccess_demo',
    'port' => 3306
];
