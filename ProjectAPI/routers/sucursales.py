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


def get_sucu():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@router.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@router.get("/sucu/", response_model=List[page_schemas.sucursal])
async def show_sucu(db:session=Depends(get_sucu)):
    sucursal = db.query(page_models.sucursales).all()
    return sucursal

@router.get("/searchsucu/{sucuname}", response_model=List[page_schemas.sucursal])
async def show_sucu_user(sucuname: str, db: session = Depends(get_sucu)):
    # Filtra los productos que coinciden con el nombre
    sucursal = db.query(page_models.sucursales).filter(page_models.sucursales.nombresucursal == sucuname).all()
    return sucursal

@router.post("/sucu/",response_model=page_schemas.sucursal)
def create_sucu(entrada:page_schemas.sucursal,db:session=Depends(get_sucu)):
    sucursal = page_models.proveedor(nombresucursal = entrada.nombresucursal, correo = entrada.correo, telefono = entrada.telefono,direccion = entrada.direccion)
    db.add(sucursal)
    db.commit()
    db.refresh(sucursal)
    return sucursal

@router.put("/sucu/{sucu_id}",response_model=page_schemas.sucursal)
def mod_sucu(sucuid: int, entrada:page_schemas.sucursal_update,db:session=Depends(get_sucu)):
    sucu = db.query(page_models.sucursales).filter_by(id=sucuid).first()
    sucu.nombresucursal = entrada.nombresucursal
    sucu.correo = entrada.correo
    sucu.telefono = entrada.telefono
    sucu.direccion = entrada.direccion
    db.commit()
    db.refresh(sucu)
    return sucu

@router.delete("/sucu/{sucu_id}",response_model=page_schemas.respuesta)
def del_sucu(sucuid: int,db:session=Depends(get_sucu)):
    elisucu = db.query(page_models.sucursales).filter_by(id=sucuid).first()
    db.delete(elisucu)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta