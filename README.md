# 🛒 BASKET-SHOP Backend

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


**Flujo principal:**
1. El administrador completa un formulario en el frontend con los datos del producto.
2. El frontend envía una solicitud **POST** al endpoint `/crear_producto`.
3. El backend valida que todos los campos requeridos estén presentes.
4. Se inserta un nuevo registro en la tabla `Productos`.
5. Se devuelve un mensaje de confirmación al administrador.

