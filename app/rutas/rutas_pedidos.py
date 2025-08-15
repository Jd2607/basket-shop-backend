from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.modelos.pedidos import pedidos
from app.database import database

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


# Obtener todos los pedidos
@router.get("/")
async def get_pedidos():
    query = pedidos.select()
    return await database.fetch_all(query)


@router.post("/crear_pedido")
async def crear_pedido(data: dict):
    # Insertar el pedido y obtener el ID generado
    query_insert = pedidos.insert().values(**data)
    last_id = await database.execute(query_insert)

    if not last_id:
        raise HTTPException(status_code=500, detail="Error al crear el pedido")

    # Buscar el pedido recién creado
    query_retorno = select(pedidos).where(pedidos.c.id == last_id)
    pedido = await database.fetch_one(query_retorno)

    return pedido