from sqlalchemy import Table, Column, Integer, String, Numeric, ForeignKey, MetaData

metadata = MetaData()

productos = Table(
    "productos",
    metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("nombre", String(29), nullable=False),
    Column("descripcion", String(70), nullable=False),
    Column("precio", Numeric(10, 2), nullable=False),
    Column("stock", Integer, nullable=False),
    Column("categoria_id", Integer, ForeignKey("categorias.id")),
)
