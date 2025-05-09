
from pydantic import BaseModel
from typing import Optional

#Entidad User
class User(BaseModel):
    id: Optional[str]
    username: str
    surname: str
    rol: str
    disabled: bool

class UserDB(User):
    password: str
