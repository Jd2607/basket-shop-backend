from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.modelos.categorias import categorias
from app.database import database

router = APIRouter(prefix="/categorias", tags=["Categorías"])


# Obtener todas las categorías
@router.get("/")
async def get_categorias():
    query = categorias.select()
    return await database.fetch_all(query)


# Crear una nueva categoría
@router.post("/crear_categoria")
async def crear_categoria(data: dict):
    query = categorias.insert().values(**data)
    await database.execute(query)
    return JSONResponse(
        status_code=200,
        content={"message": "Categoría creada exitosamente"}
    )


# Cambiar el nombre de una categoría
@router.post("/editar_categoria")
async def editar_categoria(data: dict):
    query = categorias.select().where(categorias.c.id == data["categoria_id"])
    categoriaEditar = await database.fetch_one(query)
    if categoriaEditar:
        query = categorias.update().where(categorias.c.id == data["categoria_id"]).values(nombre=data["nuevo_nombre"])
        await database.execute(query)
        return JSONResponse(
            status_code=200,
            content={"message": "Nombre de categoría actualizado exitosamente"}
        )
    else:
        return JSONResponse(
            status_code=404,
            content={"message": "Categoría no encontrada"}
        )


# Eliminar una categoría
@router.post("/eliminar_categoria")
async def eliminar_categoria(data: dict):
    query = categorias.select().where(categorias.c.id == data["id"])
    categoriaEliminar = await database.fetch_one(query)
    if categoriaEliminar:
        query = categorias.delete().where(categorias.c.id == data["id"])
        await database.execute(query)
        return JSONResponse(
            status_code=200,
            content={"message": "Categoría eliminada exitosamente"}
        )
    else:
        return JSONResponse(
            status_code=404,
            content={"message": "Categoría no encontrada"}
        )
