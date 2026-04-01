# Evidencia de pruebas con REST Client

Este proyecto fue probado con REST Client usando:

- `u1_ej_8_integrador/tests/test_api.http`

## Endpoints validados

1. Categorias: alta, listado, detalle, actualizacion, desactivacion.
2. Productos: alta, listado, detalle, actualizacion, consulta de stock, desactivacion.
3. Clientes: alta, filtros avanzados, detalle, estado de credito, pago, desactivacion.

## Criterios verificados

1. Codigos HTTP esperados en casos exitosos (`200`, `201`).
2. Manejo de errores (`400`, `404`, `409`, `422`).
3. Validaciones de schemas y reglas de negocio.

## Archivos JSON de prueba incluidos

- `u1_ej_8_integrador/tests/json/categoria_create.json`
- `u1_ej_8_integrador/tests/json/producto_create.json`
- `u1_ej_8_integrador/tests/json/cliente_create.json`
- `u1_ej_8_integrador/tests/json/filtros_clientes.json`
