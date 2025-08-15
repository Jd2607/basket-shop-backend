# app/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

# Configuración de JWT y seguridad
SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Simulación de base de datos de usuarios
usuarios_db = {
    "admin123": {
        "id": 1,
        "usuario": "admin123",
        "hashed_password": pwd_context.hash("pruebaAdmin123")
    }
}

# Funciones de utilidad
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario: str = payload.get("usuario")
        if usuario is None or usuario not in usuarios_db:
            raise HTTPException(status_code=401, detail="Usuario no válido")
        return usuarios_db[usuario]
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

# Endpoint de login
async def login(form_data: OAuth2PasswordRequestForm):
    user = usuarios_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    token = create_access_token({"usuario": user["usuario"]})
    return {"access_token": token, "token_type": "bearer"}
