import enum
from sqlalchemy import DateTime, ForeignKey, Table, Column, Integer, String, Numeric, MetaData, Enum  # 👈 aquí sí importas Enum de SQLAlchemy

metadata = MetaData()

class EstadoPedido(str, enum.Enum):
    pendiente = "pendiente"
    procesado = "procesado"
    enviado = "enviado"
    rechazado = "rechazado"

pedidos = Table(
    "pedidos",
    metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("usuario_id", Integer, ForeignKey("usuario.id")),
    Column("valorTotal", Numeric(10, 2), nullable=False),
    Column("fecha", DateTime, nullable=False),
    Column("estado", Enum(EstadoPedido, name="estado_pedido"), nullable=False),  # 👈 Aquí usamos Enum de SQLAlchemy
)
