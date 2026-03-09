-- Script de inicialización de base de datos para JVDataAccess
-- Versión: 1.0.0

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS jvdataaccess_demo
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE jvdataaccess_demo;

-- Tabla de ejemplo: Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    Identificador INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Email VARCHAR(200) UNIQUE NOT NULL,
    Edad INT,
    Activo TINYINT(1) DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de ejemplo: Productos
CREATE TABLE IF NOT EXISTS productos (
    Identificador INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    stock INT NOT NULL DEFAULT 0,
    categoria VARCHAR(100),
    activo TINYINT(1) DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de ejemplo: Clientes
CREATE TABLE IF NOT EXISTS clientes (
    Identificador INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    apellidos VARCHAR(150),
    email VARCHAR(200) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT,
    ciudad VARCHAR(100),
    codigo_postal VARCHAR(10),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de ejemplo: Pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    Identificador INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(50) DEFAULT 'pendiente',
    total DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    notas TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(Identificador) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de ejemplo: Detalles de Pedidos
CREATE TABLE IF NOT EXISTS pedidos_detalle (
    Identificador INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(Identificador) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(Identificador) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar datos de prueba
INSERT INTO productos (nombre, descripcion, precio, stock, categoria) VALUES
('Laptop Dell XPS 15', 'Portátil de alta gama con procesador Intel i7', 1299.99, 15, 'Informática'),
('Mouse Logitech MX Master 3', 'Ratón ergonómico inalámbrico', 89.99, 50, 'Periféricos'),
('Teclado Mecánico Corsair K95', 'Teclado gaming RGB con switches Cherry MX', 179.99, 30, 'Periféricos'),
('Monitor LG UltraWide 34"', 'Monitor curvo 21:9 para productividad', 599.99, 20, 'Monitores'),
('Auriculares Sony WH-1000XM4', 'Auriculares con cancelación de ruido', 349.99, 40, 'Audio');

INSERT INTO usuarios (Nombre, Apellido, Email, Edad, Activo) VALUES
('Juan', 'Pérez', 'juan.perez@example.com', 30, 1),
('María', 'González', 'maria.gonzalez@example.com', 28, 1),
('Luis', 'Martínez', 'luis.martinez@example.com', 35, 1),
('Carmen', 'López', 'carmen.lopez@example.com', 42, 0);

INSERT INTO clientes (nombre, apellidos, email, telefono, direccion, ciudad, codigo_postal) VALUES
('Juan', 'García López', 'juan.garcia@email.com', '600123456', 'Calle Mayor 123', 'Madrid', '28001'),
('María', 'Rodríguez Pérez', 'maria.rodriguez@email.com', '600234567', 'Av. Libertad 45', 'Barcelona', '08001'),
('Pedro', 'Martínez Sánchez', 'pedro.martinez@email.com', '600345678', 'Plaza España 8', 'Valencia', '46001'),
('Ana', 'López Fernández', 'ana.lopez@email.com', '600456789', 'Paseo Gracia 200', 'Barcelona', '08002'),
('Carlos', 'Sánchez Ruiz', 'carlos.sanchez@email.com', '600567890', 'Gran Vía 50', 'Madrid', '28013');

-- Insertar pedidos de ejemplo
INSERT INTO pedidos (cliente_id, estado, total) VALUES
(1, 'completado', 1389.98),
(2, 'pendiente', 949.98),
(3, 'enviado', 349.99);

-- Detalles de pedidos
INSERT INTO pedidos_detalle (pedido_id, producto_id, cantidad, precio_unitario, subtotal) VALUES
(1, 1, 1, 1299.99, 1299.99),
(1, 2, 1, 89.99, 89.99),
(2, 4, 1, 599.99, 599.99),
(2, 5, 1, 349.99, 349.99),
(3, 5, 1, 349.99, 349.99);

-- Mensaje de confirmación
SELECT '✅ Base de datos inicializada correctamente' AS mensaje;
SELECT 'Tablas creadas: usuarios, productos, clientes, pedidos, pedidos_detalle' AS info;
