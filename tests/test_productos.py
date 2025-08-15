import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_get_productos():
    with TestClient(app) as client:
        response = client.get("/productos")
        ##estado 200 significa que no hubo problemas
        assert response.status_code == 200
        #verifica que la respuesta sea una lista
        assert isinstance(response.json(), list) 
        #verifica que la lista no esté vacía
        assert len(response.json()) > 0


def test_crear_producto():
    with TestClient(app) as client:
        # Intentamos crear un nuevo producto
        producto = {"nombre": "Nuevo Producto", "descripcion":"Descripcion del producto", "precio": 100, "stock": 50, "categoria_id": 25}
        response = client.post("/productos/crear_producto", json=producto)
        assert response.status_code == 200
        assert response.json().get("message") == "Producto creado exitosamente"


def test_eliminar_producto_inexistente():
    with TestClient(app) as client:
        # Intentamos eliminar un producto que no existe
        response = client.post("/productos/eliminar_producto", json={"id": 9999})
        assert response.status_code == 404
        assert response.json().get("message") == "Producto no encontrado"


def test_eliminar_producto_existente():
    with TestClient(app) as client:
        # Intentamos eliminar un producto que existe
        response = client.post("/productos/eliminar_producto", json={"id": 1})
        assert response.status_code == 200
        assert response.json().get("message") == "Producto eliminado exitosamente"


def test_asignar_categoria_producto_inexistente():
    with TestClient(app) as client:
        # Intentamos asignar una categoría a un producto que no existe
        response = client.post("/productos/asignar_categoria", json={"producto_id": 9999, "categoria_id": 1})
        assert response.status_code == 404
        assert response.json().get("message") == "Producto no encontrado"


def test_asignar_categoria_existente():
    with TestClient(app) as client:
        # Intentamos asignar una categoría a un producto que existe
        response = client.post("/productos/asignar_categoria", json={"producto_id": 2, "categoria_id": 102}) #colocar id para prueba
        assert response.status_code == 200
        assert response.json().get("message") == "Categoría asignada al producto exitosamente"
