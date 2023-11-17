from fastapi import APIRouter, HTTPException
from typing import List
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from fastapi.params import Depends
from BD.conexion import engine, sessionlocal
import BD.schemas as page_schemas
import BD.conexion as page_conexion
import BD.models as page_models

page_models.Base.metadata.create_all(bind=engine)
router = APIRouter()


def get_car():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@router.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@router.get("/car/", response_model=List[page_schemas.Car])
async def show_car(db:session=Depends(get_car)):
    carro = db.query(page_models.Car).all()
    return carro

@router.get("/searchcar/{carname}", response_model=List[page_schemas.Car])
async def show_car_user(carname: str, db: session = Depends(get_car)):
    # Filtra los productos que coinciden con el nombre
    products = db.query(page_models.Car).filter(page_models.Car.nickname == carname).all()
    
    if not products:
        raise HTTPException(status_code=404, detail=f"No se encontraron carros para el usuario {carname}")

    # Multiplica la cantidad por el precio para cada carro encontrado
    for car in products:
        car.preciototal = car.cantidad * car.precio

    return products

@router.post("/car/",response_model=page_schemas.Car)
def create_car(entrada:page_schemas.Car,db:session=Depends(get_car)):
    carro = page_models.Car(nickname = entrada.nickname, nombreproducto = entrada.nombreproducto,stock = entrada.stock, talla = entrada.talla, cantidad = entrada.cantidad, imagen = entrada.imagen, precio = entrada.precio, categoria = entrada.categoria, nombresucursal= entrada.nombresucursal, nombreproveedor = entrada.nombreproveedor)
    db.add(carro)
    db.commit()
    db.refresh(carro)
    return carro

@router.put("/car/{car_id}",response_model=page_schemas.Car)
def mod_car(carid: int, entrada:page_schemas.car_update,db:session=Depends(get_car)):
    car = db.query(page_models.Car).filter_by(id=carid).first()
    car.nombreproducto = entrada.nombreproducto
    car.stock = entrada.stock
    car.talla = entrada.talla
    car.cantidad = entrada.cantidad
    car.imagen = entrada.imagen
    car.categoria = entrada.categoria
    car.nombresucursal = entrada.nombresucursal
    car.nombreproveedor = entrada.nombreproveedor
    db.commit()
    db.refresh(car)
    return car

@router.put("/carcanti/{cantidad_id}",response_model=page_schemas.Car)
def mod_cant(cantid: int, entrada:page_schemas.cant_update,db:session=Depends(get_car)):
    cant = db.query(page_models.Car).filter_by(id=cantid).first()
    cant.cantidad = entrada.cantidad
    db.commit()
    db.refresh(cant)
    return cant

@router.delete("/car/{car_id}",response_model=page_schemas.respuesta)
def del_car(carid: int,db:session=Depends(get_car)):
    elicar = db.query(page_models.Car).filter_by(id=carid).first()
    db.delete(elicar)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta