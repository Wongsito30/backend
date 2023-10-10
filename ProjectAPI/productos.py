from fastapi import FastAPI
from typing import List
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from fastapi.params import Depends
from BD.conexion import engine, sessionlocal
import BD.schemas as page_schemas
import BD.conexion as page_conexion
import BD.models as page_models

page_models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_product():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@app.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@app.get("/products/", response_model=List[page_schemas.Product])
async def show_product(db:session=Depends(get_product)):
    productos = db.query(page_models.Products).all()
    return productos

@app.post("/products/",response_model=page_schemas.Product)
def create_product(entrada:page_schemas.Product,db:session=Depends(get_product)):
    producto = page_models.Products(nombreproducto = entrada.nombreproducto,stock = entrada.stock, talla = entrada.talla, precio = entrada.precio, descripcion = entrada.descripcion, imagen = entrada.imagen)
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto

@app.put("/products/{producto_id}",response_model=page_schemas.Product)
def mod_product(productoid: int, entrada:page_schemas.product_update,db:session=Depends(get_product)):
    producto = db.query(page_models.Products).filter_by(id=productoid).first()
    producto.nombreproducto = entrada.nombreproducto
    producto.stock = entrada.stock
    producto.talla = entrada.talla
    producto.precio = entrada.precio
    producto.descripcion = entrada.descripcion
    producto.imagen = entrada.imagen
    db.commit()
    db.refresh(producto)
    return producto

@app.delete("/products/{producto_id}",response_model=page_schemas.respuesta)
def del_product(productoid: int,db:session=Depends(get_product)):
    eliproducto = db.query(page_models.Products).filter_by(id=productoid).first()
    db.delete(eliproducto)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta