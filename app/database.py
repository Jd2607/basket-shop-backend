from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from databases import Database

# Cambia estos valores por los de tu entorno
DATABASE_URL = "mysql+mysqlconnector://root:Juan@2607@localhost:3306/pruebas_tecnica_temporal"

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL, pool_pre_ping=True)  # pool_pre_ping evita errores de conexiones muertas

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
