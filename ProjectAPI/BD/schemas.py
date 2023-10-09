from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
     id: Optional[int]
     username: str
     contrasena: str
     correo: str
     estado: int
     
     class Config:
       from_attributes = True

class User_update(BaseModel):
     username: str
   
     
     class Config:
       from_attributes = True

class repuesta(BaseModel):
     mensaje: str