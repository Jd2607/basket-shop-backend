import pytest
from fastapi.testclient import TestClient
from app.main import app

# Test para obtener todas las categorías

def test_get_categorias():
    with TestClient(app) as client:
        response = client.get("/categorias")
        ##estado 200 significa que no hubo problemas
        assert response.status_code == 200
        #verifica que la respuesta sea una lista
        assert isinstance(response.json(), list) 
        #verifica que la lista no esté vacía
        assert len(response.json()) > 0

"""
def test_crear_categoria():
    with TestClient(app) as client:
        #accedemos a la ruta enviandole una categoria
        response = client.post("/crear_categoria", json={"nombre": "Nueva Categoria"})
        #estado 200 significa que se creó una nueva categoría
        assert response.status_code == 200
        #verificamos que la respuesta contenga un mensaje
        assert response.json().get("message") == "Categoría creada exitosamente"
"""

def test_editar_categoria_inexistente():
    with TestClient(app) as client:
        #accedemos a la ruta enviandole una categoria y el nuevo nombre
        response = client.post("/editar_categoria", json={"categoria_id": 9999, "nuevo_nombre": "Categoria Editada"})
        #estado 200 significa que se editó la categoría
        assert response.status_code == 404
        #verificamos que la respuesta contenga un mensaje
        assert response.json().get("message") == "Categoría no encontrada"


def test_editar_categoria_existente():
    with TestClient(app) as client:
        #accedemos a la ruta enviandole una categoria y el nuevo nombre
        #de prueba le enviamos la categoria 25 (Sin categoria)
        response = client.post("/editar_categoria", json={"categoria_id": 25, "nuevo_nombre": "Categoria Editada"})
        #estado 200 significa que se editó la categoría
        assert response.status_code == 200
        #verificamos que la respuesta contenga un mensaje
        assert response.json().get("message") == "Nombre de categoría actualizado exitosamente"


def test_eliminar_categoria_inexistente():
    with TestClient(app) as client:
        # Intentamos eliminar una categoría que no existe
        response = client.post("/eliminar_categoria", json={"id": 9999})
        assert response.status_code == 404
        assert response.json().get("message") == "Categoría no encontrada"


def test_eliminar_categoria_existente():
    with TestClient(app) as client:
        # Intentamos eliminar una categoría que existe
        response = client.post("/eliminar_categoria", json={"id": 1})
        assert response.status_code == 200
        assert response.json().get("message") == "Categoría eliminada exitosamente"