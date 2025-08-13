# 🛒🏀 BASKET-SHOP Backend

- Repositorio del backend de MiTienda, una aplicación web de ventas desarrollada como prueba técnica
- Esta solución está construida con Python, FastAPI, SQLAlchemy, MySQL y una arquitectura de microservicios.


## FUNCIONALIDAD

- Manejo de sesiones
- CRUD para los productos
- CRUD para las categorias


## CASO DE USO: Crear Producto

**ID:** CU-007  
**Nombre del caso de uso:** Crear Producto  
**Actor principal:** Administrador  
**Descripción:**  
El administrador agrega un nuevo producto al sistema a través del frontend. El backend valida la información y lo registra en la base de datos bajo la categoría correspondiente.


### Flujo Principal

| Paso | Actor       | Acción |
|------|------------|--------|
| 1    | Administrador | Completa un formulario en el frontend con los datos del producto |
| 2    | Administrador | Envía una solicitud **POST** al endpoint `/crear_producto` |
| 3    | Sistema       | Valida que todos los campos requeridos estén presentes |
| 4    | Sistema       | Inserta un nuevo registro en la tabla `Productos` |
| 5    | Sistema       | Devuelve un mensaje de confirmación al administrador |
