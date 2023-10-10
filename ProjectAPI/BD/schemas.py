from pydantic import BaseModel
from typing import Optional
from datetime import date

class User(BaseModel):
     id: Optional[int] = None
     nickname: str
     contrasena: str
     email: str
     estado: int
     
     class Config:
       from_attributes = True

class User_update(BaseModel):
     nickname: str
   
     
     class Config:
       from_attributes = True

class Product(BaseModel):
     id: Optional[int] = None
     nombreproducto: str
     stock: int
     talla: str
     precio: float
     descripcion: str
     imagen: Optional[bytes]
     
     class Config:
       from_attributes = True

class product_update(BaseModel):
     nombreproducto: str
     stock: int
     talla: str
     precio: float
     descripcion: str
     imagen: Optional[bytes]
   
     
     class Config:
       from_attributes = True

class Car(BaseModel):
     id: Optional[int] = None
     nickname: str
     nombreproducto: str
     stock: int
     talla: str
     cantidad: int
     preciototal: float
     imagen: Optional[bytes]
     
     class Config:
       from_attributes = True

class car_update(BaseModel):
      nickname: str
      nombreproducto: str
      stock: int
      talla: str
      cantidad: int
      preciototal: float
      imagen: Optional[bytes]
      
      class Config:
       from_attributes = True

class Wishlist(BaseModel):
     id: Optional[int] = None
     nickname: str
     nombreproducto: str
     stock: int
     talla: str
     cantidad: int
     imagen: Optional[bytes]
     
     class Config:
       from_attributes = True

class Wishlist_update(BaseModel):
      nickname: str
      nombreproducto: str
      stock: int
      talla: str
      cantidad: int
      imagen: Optional[bytes]
      
      class Config:
       from_attributes = True

class Direction(BaseModel):
     id: Optional[int] = None
     nickname: str
     nombrecalle: str
     numerocasa: int
     cp: int
     colonia: str
     municipio: str
     estado: str
     
     class Config:
       from_attributes = True

class Direction_update(BaseModel):
      nickname: str
      nombrecalle: str
      numerocasa: int
      cp: int
      colonia: str
      municipio: str
      estado: str
      
      class Config:
       from_attributes = True

class pagos(BaseModel):
     id: Optional[int] = None
     nombretarjeta: str
     numerotarjeta: str
     fecha: date
     cvv: int
     nickname: str
     
     class Config:
       from_attributes = True

class pagos_update(BaseModel):
      nombretarjeta: str
      numerotarjeta: str
      fecha: date
      cvv: int
      nickname: str
      
      class Config:
       from_attributes = True

class proveedor(BaseModel):
     id: Optional[int] = None
     nombreproveedor: str
     procedencia: str
     telefono: str
     correo: str
     
     class Config:
       from_attributes = True

class proveedor_update(BaseModel):
      nombreproveedor: str
      procedencia: str
      telefono: str
      correo: str
      
      class Config:
       from_attributes = True

class respuesta(BaseModel):
     mensaje: str