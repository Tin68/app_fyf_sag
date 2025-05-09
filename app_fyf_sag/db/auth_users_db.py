from typing import Annotated
import reflex as rx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
#from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from app_fyf_sag.db.schemas.user import user_schema, users_schema
from app_fyf_sag.styles import utils
from app_fyf_sag.db.client import db_client
from app_fyf_sag.db.models.user import User, UserDB
import bcrypt 


ALGORITHM = utils.login_algorithm
ACCESS_TOKEN_DURATION = utils.login_access_token_duration
SECRET = utils.login_secret

auth_db_router = APIRouter(prefix="/logindb",
                   tags=["logindb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="logindb")

crypt = CryptContext(schemes="bcrypt")

# Inicia el server : uvicorn basic_aut_users:app  --reload


def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}

def search_userdb(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        
        return UserDB(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}   
''' 
def search_user(field: str, key):
    #bytes = key.encode('utf-8') 
    #salt = bcrypt.gensalt() 
    #user_encode = bcrypt.hashpw(bytes, salt).decode('utf-8')#lo convierte en str
    #print(user_encode)
    for user in db_client.users.find():
        result = bcrypt.checkpw(key.encode('utf-8'),user.get("username").encode('utf-8')) 
        print (result)
        if result:
            print (user)
            return User(**user_schema(user))                    
    return {"error": "No se ha encontrado el usuario"}
        
def search_userdb(field: str, key):
    for user in db_client.users.find():
        result = bcrypt.checkpw(key.encode('utf-8'),user.get("username").encode('utf-8')) 
        print (result)
        if result:
            print (user)
            return UserDB(**user_schema(user))                    
    return {"error": "No se ha encontrado el usuario"}  
'''
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
    return search_user ("username",username)

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")        
    return user

@auth_db_router.post("") #http://127.0.0.1:8000/logindb
async def logindb(form_data: OAuth2PasswordRequestForm = Depends()):  
    print("Hola tin")  
    
    print(form_data) 
    print(form_data.username) 
    print(form_data.password) 
    if type(search_user("username", form_data.username)) == User:
        user = search_userdb ("username",form_data.username)   
    else:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND, detail="El Usuario no existe")
    #user_db = users_db.get(form.username)
    if not crypt.verify(form_data.password, user.password):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    access_token = {"sub" : user.username,
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)} #sustituye datetime.utcnow() --> datetime.now(timezone.utc)
    #return {"accss_toke" : access_token,  "token_tpe": "bearer"} #desencriptado
    return {"access_token" : jwt.encode(access_token, SECRET, algorithm = ALGORITHM) ,  "token_tpe": "bearer"} #encriptado


@auth_db_router.get("/users/me") #http://127.0.0.1:8000/logindb/users/me
async def me(user: User = Depends (current_user)):
    return user