from pydantic import BaseModel
from typing import Optional

#Entidad Sheet
class Sheet(BaseModel):
    id: Optional[str]
    num: int
    buque: str
    fecha_entrada: str
    tip_carpeta: str
    consignatario: str
    c_d: str
    doc: bool
    tip_doc: str
    prev: bool
    fecha_llegada: str
    sol: int
    estibadora: str
    prov: bool
    result_c: bool
    dil: bool
    finish_data: str
    observaciones:str
    custom_tip: str
    custom_data: str
    aduana: bool