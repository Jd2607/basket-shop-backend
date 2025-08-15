from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.modelos.producto import productos
from app.database import database

router = APIRouter(prefix="/productos", tags=["Productos"])


#ruta para obtener todos los productos
@router.get("/")
async def get_productos():
    query = productos.select()
    return await database.fetch_all(query)


#ruta para obtener un producto
@router.post("/obtener")
async def get_producto(data: dict):
    query = productos.select().where(productos.c.id == data["id"])
    return await database.fetch_one(query)




class IdsRequest(BaseModel):
    ids: List[int]

@router.post("/obtener-por-ids")
async def obtener_productos_por_ids(request: IdsRequest):
    print(request.ids)
    query = productos.select().where(productos.c.id.in_(request.ids))
    return await database.fetch_all(query)


#ruta para crear producto
@router.post("/crear_producto")
async def crear_producto(data: dict):
    query = productos.insert().values(**data)
    await database.execute(query)
    return JSONResponse(status_code=200, content={"message": "Producto creado exitosamente"})


# Ruta para asignar/cambiar categoria a un producto
@router.post("/asignar_categoria")
async def asignar_categoria(data: dict):
    query = productos.select().where(productos.c.id == data["producto_id"])
    productoAsignar = await database.fetch_one(query)
    if productoAsignar:
        query = productos.update().where(productos.c.id == data["producto_id"]).values(categoria_id=data["categoria_id"])
        await database.execute(query)
        return JSONResponse(
            status_code=200,
            content={"message": "Categoría asignada al producto exitosamente"}
        )
    else:
        return JSONResponse(
            status_code=404,
            content={"message": "Producto no encontrado"}
        )


#ruta para eliminar producto
@router.post("/eliminar_producto")
async def eliminar_producto(data: dict):
    query = productos.select().where(productos.c.id == data["id"])
    productoEliminar = await database.fetch_one(query)
    if productoEliminar:
        query = productos.delete().where(productos.c.id == data["id"])
        await database.execute(query)
        return JSONResponse(status_code=200, content={"message": "Producto eliminado exitosamente"})
    else:
        return JSONResponse(status_code=404, content={"message": "Producto no encontrado"})
