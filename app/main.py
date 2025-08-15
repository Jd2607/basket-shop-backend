from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.modelos.producto import productos
from app.modelos.usuario import usuarios
from app.modelos.categorias import categorias
from fastapi.middleware.cors import CORSMiddleware
from app.modelos.categoriaModel import CategoriaModelo
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional

from app.database import database  # Solo usamos el objeto database

app = FastAPI()

# Configuración de CORS 
SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Configuración de seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Simulación de base de datos
usuarios_db = {
    "admin123": {
        "id": 1,
        "usuario": "admin123",
        "hashed_password": pwd_context.hash("pruebaAdmin123")
    }
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None or email not in usuarios_db:
            raise HTTPException(status_code=401, detail="Usuario no válido")
        return usuarios_db[email]
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

# Endpoint para login y generar token
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = usuarios_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    token = create_access_token({"usuario": user["usuario"]})
    return {"access_token": token, "token_type": "bearer"}

# Configuración de CORS para peticiones 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],         # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],         # cabeceras permitidas
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Ruta de prueba
@app.get("/")
async def read_root():
    return {"message": "Hola FastAPI con MySQL"}

# Ruta get para obtener todos los productos registrados
@app.get("/productos")
async def get_productos():
    query = productos.select()
    return await database.fetch_all(query)

# Ruta para crear un producto
@app.post("/productos/crear_producto")
async def crear_producto(data: dict):
    query = productos.insert().values(**data)
    await database.execute(query)
    return JSONResponse(
        status_code=200,
        content={"message": "Producto creado exitosamente"}
    )

# Ruta para asignar/cambiar categoria a un producto
@app.post("/productos/asignar_categoria")
async def asignar_categoria(data: dict):
    query = productos.select().where(productos.c.id == data["producto_id"])
    productoAsignar = await database.fetch_one(query)
    if productoAsignar:
        query = productos.update().where(productos.c.id == data["producto_id"]).values(categoria_id=data["categoria_id"])
        await database.execute(query)
        return JSONResponse(
            status_code=200,
            content={"message": "Categoría asignada al producto exitosamente"}
        )
    else:
        return JSONResponse(
            status_code=404,
            content={"message": "Producto no encontrado"}
        )

# Ruta para eliminar un producto
@app.post("/productos/eliminar_producto")
async def eliminar_producto(data: dict):
    query = productos.select().where(productos.c.id == data["id"])
    productoEliminar = await database.fetch_one(query)
    if productoEliminar:
        query = productos.delete().where(productos.c.id == data["id"])
        await database.execute(query)
        return JSONResponse(
            status_code=200,
            content={"message": "Producto eliminado exitosamente"}
        )
    else:
        return JSONResponse(
            status_code=404,
            content={"message": "Producto no encontrado"}
        )

# Ruta get para obtener todos los usuarios
@app.get("/usuarios")
async def get_usuarios():
    query = usuarios.select()
    return await database.fetch_all(query)

# Ruta para obtener las categorias
@app.get("/categorias")
async def get_categorias():
    query = categorias.select()
    return await database.fetch_all(query)

# Ruta para crear una categoria
@app.post("/categorias/crear_categoria")
async def crear_categoria(categoria: dict):
    query = categorias.insert().values(**categoria)
    await database.execute(query)
    return JSONResponse(
        status_code=200,
        content={"message": "Categoría creada exitosamente"}
    )

# Ruta para cambiar el nombre de una categoria
@app.post("/categorias/editar_categoria")
async def cambiar_nombre_categoria(data: dict):
    query = categorias.select().where(categorias.c.id == data["categoria_id"])
    categoriaEditar = await database.fetch_one(query)
    if categoriaEditar:
        query = categorias.update().where(categorias.c.id == data["categoria_id"]).values(nombre=data["nuevo_nombre"])
        await database.execute(query)
        return JSONResponse(
            status_code=200,
            content={"message": "Nombre de categoría actualizado exitosamente"}
        )
    else:
        return JSONResponse(
            status_code=404,
            content={"message": "Categoría no encontrada"}
        )

# Ruta para eliminar una categoria
@app.post("/categorias/eliminar_categoria")
async def eliminar_categoria(categoria: dict):
    query = categorias.select().where(categorias.c.id == categoria["id"])
    categoriaEliminar = await database.fetch_one(query)
    if categoriaEliminar:
        query = categorias.delete().where(categorias.c.id == categoria["id"])
        await database.execute(query)
        return JSONResponse(
            status_code=200,
            content={"message": "Categoría eliminada exitosamente"}
        )
    else:
        return JSONResponse(
            status_code=404,
            content={"message": "Categoría no encontrada"}
        )

# Probar la conexión a la base de datos
@app.get("/test-db")
async def test_db():
    query = "SELECT VERSION()"
    result = await database.fetch_one(query=query)
    return {"mysql_version": result[0] if result else "No se pudo conectar"}

