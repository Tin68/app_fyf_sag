
from pydantic import BaseModel
from typing import Optional
from typing import TypedDict

#Entidad User
class User(BaseModel): #class User(TypedDict):
    id: Optional[str]
    username: str
    surname: str
    rol: str
    disabled: bool

class UserDB(User):
    password: str
