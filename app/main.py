from fastapi import FastAPI
from app.database import database, metadata, engine
from app.modelos.producto import productos
from app.modelos.usuario import usuarios
from app.modelos.categorias import categorias
from fastapi.middleware.cors import CORSMiddleware
from app.modelos.categoriaModel import CategoriaModelo
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional



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




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia * por tu dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configuración de la base de datos
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



#ruta de prueba
@app.get("/")
async def read_root():
    return {"message": "Hola FastAPI con MySQL"}




#ruta get para obtener todos los productos registrados
@app.get("/productos")
async def get_productos():
    query = productos.select()
    #se usa fetch ya que esperamos un valor de vuelta
    return await database.fetch_all(query)
    


#ruta para crear un producto
@app.post("/crear_producto")
async def crear_producto(data: dict):
    query = productos.insert().values(**data)
    await database.execute(query)
    return {"message": "Producto creado exitosamente"}


#ruta get para obtener todos los usuarios
@app.get("/usuarios")
async def get_usuarios():
    query = usuarios.select()
    return await database.fetch_all(query)



#ruta para obtener las categorias
@app.get("/categorias")
async def get_categorias():
    query = categorias.select()
    return await database.fetch_all(query)



#ruta para crear una categoria
@app.post("/crear_categoria")
#de parametro recibimos un diccionario
async def crear_categoria(categoria: dict):
    # ** sirve para desestructurar el diccionario como se hace con JSON
    query = categorias.insert().values(**categoria)
    #usamos execute ya que no esperamos un valor de vuelta
    await database.execute(query)
    return {"message": "Categoría creada exitosamente"}



#ruta para cambiar el nombre de una categoria
@app.post("/editar_categoria")
#usamos el modelo creado el cual se llenara con la informacion que recibimos
async def cambiar_nombre_categoria(data: dict):
    #categorias.c hace referencia a las columnas de la tabla
    query = categorias.select().where(categorias.c.id == data["categoria_id"])
    categoriaEditar = await database.fetch_one(query)
    if categoriaEditar:
        query = categorias.update().where(categorias.c.id == data["categoria_id"]).values(nombre=data["nuevo_nombre"])
        await database.execute(query)
        return {"message": "Nombre de categoría actualizado exitosamente"}
    else:
        return {"message": "Categoría no encontrada"}
    


#ruta para asignar/cambiar categoria a un producto
@app.post("/asignar_categoria")
async def asignar_categoria(data: dict):
    query = productos.select().where(productos.c.id == data["producto_id"])
    productoAsignar = database.fetch_one(query)
    if productoAsignar:
        query = productos.update().where(productos.c.id == data["producto_id"]).values(categoria_id=data["categoria_id"])
        await database.execute(query)
        return {"message": "Categoría asignada al producto exitosamente"}




#ruta para eliminar una categoria
@app.post("/eliminar_categoria")
async def eliminar_categoria(categoria: dict):
    query = categorias.select().where(categorias.c.id == categoria["id"])
    categoriaEliminar = await database.fetch_one(query)
    if categoriaEliminar:
        query = categorias.delete().where(categorias.c.id == categoria["id"])
        await database.execute(query)
        return {"message": "Categoría eliminada exitosamente"}
    else:
        return {"message": "Categoría no encontrada"}





##probamos la conexion a la base de datos
@app.get("/test-db")
async def test_db():
    query = "SELECT VERSION()"
    result = await database.fetch_one(query=query)
    return {"mysql_version": result[0] if result else "No se pudo conectar"}

