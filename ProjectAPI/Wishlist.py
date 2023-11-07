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


def get_wish():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@app.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@app.get("/wish/", response_model=List[page_schemas.Wishlist])
async def show_wish(db:session=Depends(get_wish)):
    wishlist = db.query(page_models.Wishlist).all()
    return wishlist

@app.get("/searchfav/{favname}", response_model=List[page_schemas.Wishlist])
async def show_fav_user(favname: str, db: session = Depends(get_wish)):
    # Filtra los productos que coinciden con el nombre
    products = db.query(page_models.Wishlist).filter(page_models.Wishlist.nickname == favname).all()
    return products

@app.post("/wish/",response_model=page_schemas.Wishlist)
def create_wish(entrada:page_schemas.Wishlist,db:session=Depends(get_wish)):
    wishlist = page_models.Wishlist(nickname = entrada.nickname, nombreproducto = entrada.nombreproducto,stock = entrada.stock, talla = entrada.talla, cantidad = entrada.cantidad, imagen = entrada.imagen, categoria = entrada.categoria, nombreproveedor = entrada.nombreproveedor, nombresucursal = entrada.nombresucursal)
    db.add(wishlist)
    db.commit()
    db.refresh(wishlist)
    return wishlist

@app.put("/wish/{wish_id}",response_model=page_schemas.Wishlist)
def mod_wish(wishid: int, entrada:page_schemas.Wishlist_update,db:session=Depends(get_wish)):
    wish = db.query(page_models.Wishlist).filter_by(id=wishid).first()
    wish.nombreproducto = entrada.nombreproducto
    wish.stock = entrada.stock
    wish.talla = entrada.talla
    wish.cantidad = entrada.cantidad
    wish.imagen = entrada.imagen
    wish.categoria = entrada.categoria
    wish.nombreproveedor = entrada.nombreproveedor
    wish.nombresucursal = entrada.nombresucursal
    db.commit()
    db.refresh(wish)
    return wish

@app.delete("/wish/{wish_id}",response_model=page_schemas.respuesta)
def del_wish(wishid: int,db:session=Depends(get_wish)):
    eliwish = db.query(page_models.Wishlist).filter_by(id=wishid).first()
    db.delete(eliwish)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta