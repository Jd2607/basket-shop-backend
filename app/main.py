from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from app.database import database
from app.rutas import rutas_productos, rutas_categorias, rutas_pedidos, rutas_pedido_productos
from app.autenticacion import login


app = FastAPI()


# Registrar routers
app.include_router(rutas_productos.router)
app.include_router(rutas_categorias.router)
app.include_router(rutas_pedidos.router)
app.include_router(rutas_pedido_productos.router)


# Ruta de login
@app.post("/login")
async def login_route(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login(form_data)


# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      
    allow_credentials=True,
    allow_methods=["*"],      
    allow_headers=["*"],      
)


# Conexión y desconexión a la base de datos
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


# Probar la conexión a la base de datos
@app.get("/test-db")
async def test_db():
    query = "SELECT VERSION()"
    result = await database.fetch_one(query=query)
    return {"mysql_version": result[0] if result else "No se pudo conectar"}