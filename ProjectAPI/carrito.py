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


def get_car():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@app.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@app.get("/car/", response_model=List[page_schemas.Car])
async def show_car(db:session=Depends(get_car)):
    carro = db.query(page_models.Car).all()
    return carro

@app.post("/car/",response_model=page_schemas.Car)
def create_car(entrada:page_schemas.Car,db:session=Depends(get_car)):
    carro = page_models.Car(nickname = entrada.nickname, nombreproducto = entrada.nombreproducto,stock = entrada.stock, talla = entrada.talla, cantidad = entrada.cantidad, preciototal = entrada.preciototal, imagen = entrada.imagen)
    db.add(carro)
    db.commit()
    db.refresh(carro)
    return carro

@app.put("/car/{car_id}",response_model=page_schemas.Car)
def mod_car(carid: int, entrada:page_schemas.car_update,db:session=Depends(get_car)):
    car = db.query(page_models.Car).filter_by(id=carid).first()
    car.nombreproducto = entrada.nombreproducto
    car.stock = entrada.stock
    car.talla = entrada.talla
    car.cantidad = entrada.cantidad
    car.preciototal = entrada.preciototal
    car.imagen = entrada.imagen
    db.commit()
    db.refresh(car)
    return car

@app.delete("/car/{car_id}",response_model=page_schemas.respuesta)
def del_car(carid: int,db:session=Depends(get_car)):
    elicar = db.query(page_models.Car).filter_by(id=carid).first()
    db.delete(elicar)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta