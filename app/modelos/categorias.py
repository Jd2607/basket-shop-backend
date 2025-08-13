from sqlalchemy import Table, Column, Integer, String, Numeric, ForeignKey, MetaData

metadata = MetaData()

categorias = Table(
    "categorias",
    metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("nombre", String(50), nullable=False),
)