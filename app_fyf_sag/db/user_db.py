from fastapi import APIRouter, HTTPException, status#, FastAPI
from bson import ObjectId
from app_fyf_sag.db.models.user import User, UserDB
from app_fyf_sag.db.schemas.user import user_schema, users_schema
from app_fyf_sag.db.client import db_client


items_router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

# Inicia el server : uvicorn usersdb:app --reload

@items_router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

# Path()
@items_router.get("/{id}") 
async def user(id: str):
    return search_user("_id", ObjectId(id))


# Query
@items_router.get("/")  # Query
async def user(id: str):
    return search_user("_id", ObjectId(id))


@items_router.post("/", response_model=UserDB, status_code=status.HTTP_201_CREATED)
async def user(user: UserDB):
    if type(search_user("surname", user.surname)) == User:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND, detail="El usuario ya existe")
    user_dict = dict(user)
    del user_dict["id"] #xq mongodb lo genera automaticamente
    id = db_client.users.insert_one(user_dict).inserted_id #lo crea y acedo a su id
    new_user = user_schema(db_client.users.find_one({"_id": id})) #_id es el nombre que da mongodb
    return UserDB(**new_user)

@items_router.put("/", response_model=UserDB)
async def user(userdb: UserDB):
    print(userdb)
    user_dict_put = dict(userdb)
    del user_dict_put["id"]
    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(userdb.id)}, user_dict_put)
    except:
        return {"error": "No se ha actualizado el usuario"}
    return search_userdb("_id", ObjectId(userdb.id))

@items_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"error": "No se ha eliminado el usuario"}

# Helper
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