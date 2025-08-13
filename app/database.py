from sqlalchemy import create_engine, MetaData
from databases import Database

DATABASE_URL = "mysql+mysqlconnector://root:Juan@2607@localhost:3306/prueba_tecnica"

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)