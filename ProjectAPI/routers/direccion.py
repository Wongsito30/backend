from fastapi import APIRouter
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


def get_direction():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@router.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@router.get("/direction/", response_model=List[page_schemas.Direction])
async def show_direction(db:session=Depends(get_direction)):
    direccion = db.query(page_models.Direction).all()
    return direccion

@router.get("/searchcalle/{callename}", response_model=List[page_schemas.Direction])
async def show_calle_user(callename: str, db: session = Depends(get_direction)):
    # Filtra los productos que coinciden con el nombre
    direccion = db.query(page_models.Direction).filter(page_models.Direction.nombrecalle == callename).all()
    return direccion

@router.get("/searchdir/{dirname}", response_model=List[page_schemas.Direction])
async def show_dir_user(dirname: str, db: session = Depends(get_direction)):
    # Filtra los productos que coinciden con el nombre
    direccion = db.query(page_models.Direction).filter(page_models.Direction.nickname == dirname).all()
    return direccion

@router.post("/direction/",response_model=page_schemas.Direction)
def create_direction(entrada:page_schemas.Direction,db:session=Depends(get_direction)):
    direccion = page_models.Direction(nombrecalle = entrada.nombrecalle,numerocasa = entrada.numerocasa, cp = entrada.cp, colonia = entrada.colonia, municipio = entrada.municipio, estado = entrada.estado, nickname = entrada.nickname)
    db.add(direccion)
    db.commit()
    db.refresh(direccion)
    return direccion

@router.put("/direction/{direction_id}",response_model=page_schemas.Direction)
def mod_direction(directionid: int, entrada:page_schemas.Direction_update,db:session=Depends(get_direction)):
    direccion = db.query(page_models.Direction).filter_by(id=directionid).first()
    direccion.nombrecalle = entrada.nombrecalle
    direccion.numerocasa = entrada.numerocasa
    direccion.cp = entrada.cp
    direccion.colonia = entrada.colonia
    direccion.municipio = entrada.municipio
    direccion.estado = entrada.estado
    direccion.nickname = entrada.nickname
    db.commit()
    db.refresh(direccion)
    return direccion

@router.delete("/direction/{direction_id}",response_model=page_schemas.respuesta)
def del_direction(directionid: int,db:session=Depends(get_direction)):
    elidireccion = db.query(page_models.Direction).filter_by(id=directionid).first()
    db.delete(elidireccion)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta