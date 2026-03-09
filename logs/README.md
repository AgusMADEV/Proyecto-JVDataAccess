# Directorio de Logs

Este directorio contiene los archivos de log generados por el sistema de logging de JVDataAccess v2.0.

## Formato de Archivos

Los logs se guardan con el formato: `{nombre_logger}_{fecha}.log`

Ejemplo:
- `JVDB2_2026-03-09.log`
- `JVPool_2026-03-09.log`

## Contenido de los Logs

Los logs registran:
- Conexiones a la base de datos
- Consultas SQL ejecutadas
- Parámetros de las consultas
- Transacciones (BEGIN, COMMIT, ROLLBACK)
- Errores y advertencias
- Información del pool de conexiones

## Ejemplo de Log

```
2026-03-09 10:30:45 - JVDB2 - INFO - Conexión exitosa a localhost/mi_base_datos
2026-03-09 10:30:46 - JVDB2 - INFO - SQL: SELECT * FROM usuarios WHERE Activo = %s | Params: (1,)
2026-03-09 10:30:46 - JVDB2 - INFO - 25 registros seleccionados de 'usuarios'
2026-03-09 10:30:47 - JVDB2 - INFO - Transacción: BEGIN
2026-03-09 10:30:48 - JVDB2 - INFO - Transacción: COMMIT
```

## Configuración

Puedes configurar el logging al crear la instancia de JVDB2:

**Python:**
```python
log_config = {
    'log_dir': 'logs',
    'log_level': logging.INFO,
    'console_output': True,
    'file_output': True
}

db = JVDB2(..., log_config=log_config)
```

**PHP:**
```php
$logConfig = [
    'log_dir' => 'logs',
    'log_level' => JVLogger::INFO,
    'console_output' => true,
    'file_output' => true
];

$db = new JVDB2(..., $logConfig);
```

## Mantenimiento

- Los logs se crean automáticamente cuando se usa JVDB2
- Se crea un archivo nuevo cada día
- Se recomienda implementar rotación de logs para evitar archivos muy grandes
- Puedes eliminar logs antiguos manualmente o con scripts automatizados

## .gitignore

Los archivos de log (*.log) están excluidos del control de versiones mediante .gitignore.
