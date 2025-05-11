from pydantic import BaseModel
from typing import Optional

#Entidad formdata
class formdata(BaseModel):
    grant_type: Optional[str]
    username: str
    password: str
    client_id: Optional[str]
    client_secret: Optional[str]
    scopes: Optional[str]