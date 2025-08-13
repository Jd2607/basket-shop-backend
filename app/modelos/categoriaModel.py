from pydantic import BaseModel

class CategoriaModelo(BaseModel):
    categoria_id: int
    nuevo_nombre: str