from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.modelos.pedido_producto import pedido_productos
from app.database import database

router = APIRouter(prefix="/pedido_productos", tags=["Pedidos_productos"])


# Obtener todos los productos de un pedido
@router.post("/obtener")
async def get_pedidos_productos(data: dict):
    query = pedido_productos.select().where(pedido_productos.c.pedido_id == data["pedido_id"])
    return await database.fetch_all(query)


#crear pedido productos
@router.post("/crear")
async def crear_pedido_producto(data: dict):
    query = pedido_productos.insert().values(**data)
    return await database.execute(query)