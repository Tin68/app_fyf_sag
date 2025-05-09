import reflex as rx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from app_fyf_sag.styles import utils
from app_fyf_sag.db.client import db_client
from app_fyf_sag.db.models.user import User, UserDB


ALGORITHM = utils.login_algorithm
ACCESS_TOKEN_DURATION = utils.login_access_token_duration
SECRET = utils.login_secret

auth_router = APIRouter(prefix="/login",
                   tags=["login"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes="bcrypt")

# Inicia el server : uvicorn basic_aut_users:app  --reload

#Entidad User

class User(BaseModel):
    username: str
    surname: str
    rol: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "S24237Z" :{
        "username" : "S24237Z",
        "surname" : "Lata",
        "rol" : "admin",
        "disabled" : False,
        "password" : "$2a$12$cpqgYXMCvuw8WC0CfpdhwetHRicMZvp.YHnbBfPG7MWBj749BHwK2"
    },
    "K99987W" :{
        "username" : "K99987W",
        "surname" : "Enrique",
        "rol" : "user",
        "disabled" : True,
        "password" : "$2a$12$hMr5R5Jg.isqTiP0GQHQSu/crJwS9w2AEab5RSo1ACcYAInkUjSXu"
    },
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])     


async def auth_user(token : str = Depends(oauth2)):
    exception = HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales de autenticacion invalidas",
                headers= {"WWW-Autenticate" : "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms = [ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except : #PyJWTError:
        raise exception
    
    return search_user (username)

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")        
    return user

@auth_router.post("") #http://127.0.0.1:8000/login
async def login(form: OAuth2PasswordRequestForm = Depends()):
    print(form.username)
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="El Usuario no es correcto")
    
    user = search_user_db (form.username)    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    access_token = {"sub" : user.username,
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)} #sustituye datetime.utcnow() --> datetime.now(timezone.utc)
    
    #return {"accss_toke" : access_token,  "token_tpe": "bearer"} #desencriptado
    return {"accss_toke" : jwt.encode(access_token, SECRET, algorithm = ALGORITHM) ,  "token_tpe": "bearer"} #encriptado


@auth_router.get("/users/me") #http://127.0.0.1:8001/login/users/me
async def me(user: User = Depends (current_user)):
    return user