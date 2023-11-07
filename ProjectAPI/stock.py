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


def get_stock():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@app.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@app.get("/stock/", response_model=List[page_schemas.stock])
async def show_stock(db:session=Depends(get_stock)):
    stock = db.query(page_models.Stock).all()
    return stock

@app.get("/searchstock/{stockid}", response_model=List[page_schemas.stock])
async def show_stock_user(stockid: str, db: session = Depends(get_stock)):
    # Filtra los productos que coinciden con el nombre
    stock = db.query(page_models.Stock).filter(page_models.Stock.id == stockid).all()
    return stock

@app.post("/stock/",response_model=page_schemas.stock)
def create_stock(entrada:page_schemas.stock,db:session=Depends(get_stock)):
    stock = page_models.Stock(stockcant = entrada.stockcant, nombreproducto = entrada.nombreproducto, talla = entrada.talla,nombresucursal = entrada.nombresucursal,nombreproveedor = entrada.nombreproveedor)
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock

@app.put("/stock/{stock_id}",response_model=page_schemas.stock)
def mod_stock(stockid: int, entrada:page_schemas.stock_update,db:session=Depends(get_stock)):
    stock = db.query(page_models.Stock).filter_by(id=stockid).first()
    stock.stockcant = entrada.stockcant
    stock.nombreproducto = entrada.nombreproducto
    stock.talla = entrada.talla
    stock.nombresucursal = entrada.nombresucursal
    stock.nombreproveedor = entrada.nombreproveedor
    db.commit()
    db.refresh(stock)
    return stock

@app.delete("/stock/{stock_id}",response_model=page_schemas.respuesta)
def del_stock(stockid: int,db:session=Depends(get_stock)):
    elistock = db.query(page_models.Stock).filter_by(id=stockid).first()
    db.delete(elistock)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta