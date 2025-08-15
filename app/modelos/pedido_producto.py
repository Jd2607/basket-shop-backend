from sqlalchemy import DateTime, ForeignKey, Table, Column, Integer, String, Numeric, MetaData, Enum  # 👈 aquí sí importas Enum de SQLAlchemy

metadata = MetaData()



pedido_productos = Table(
    "pedido_productos",
    metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("pedido_id", Integer, ForeignKey("pedido.id")),
    Column("producto_id", Integer, ForeignKey("producto.id")),
    Column("cantidad", Integer, nullable=False),
    Column("precio_unitario", Numeric(10, 2), nullable=False),
)
