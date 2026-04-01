# Checklist Swagger UI

1. Iniciar API en `http://127.0.0.1:8000`.
2. Abrir `http://127.0.0.1:8000/docs`.
3. Verificar que aparezcan los tags: Categorias, Productos, Clientes.
4. Ejecutar `POST /categorias/` con payload valido y confirmar `201`.
5. Ejecutar `POST /productos/` con payload valido y confirmar `201`.
6. Ejecutar `POST /clientes/` con payload valido y confirmar `201`.
7. Ejecutar `GET /clientes/` con filtros y confirmar resultado.
8. Ejecutar `PUT /clientes/{id}/pagar` y confirmar actualizacion de riesgo.
9. Ejecutar un caso invalido para ver error `400/409/422`.
10. Confirmar en los schemas que los campos y tipos coincidan con el enunciado.
