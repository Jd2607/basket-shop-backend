from sqlalchemy import Table, Column, Integer, String, Numeric, ForeignKey, MetaData

metadata = MetaData()

usuarios = Table(
    "usuarios",
    metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("nombre", String(100), nullable=False),
    Column("contraseña", String(255), nullable=False),
)