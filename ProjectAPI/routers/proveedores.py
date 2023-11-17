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


def get_prov():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@router.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@router.get("/prov/", response_model=List[page_schemas.proveedor])
async def show_prov(db:session=Depends(get_prov)):
    proveedor = db.query(page_models.proveedor).all()
    return proveedor

@router.get("/searchpro/{proname}", response_model=List[page_schemas.proveedor])
async def show_pro_user(proname: str, db: session = Depends(get_prov)):
    # Filtra los productos que coinciden con el nombre
    proveedor = db.query(page_models.proveedor).filter(page_models.proveedor.nombreproveedor == proname).all()
    return proveedor

@router.post("/prov/",response_model=page_schemas.proveedor)
def create_prov(entrada:page_schemas.proveedor,db:session=Depends(get_prov)):
    proveedor = page_models.proveedor(nombreproveedor = entrada.nombreproveedor,procedencia = entrada.procedencia, telefono = entrada.telefono, correo = entrada.correo)
    db.add(proveedor)
    db.commit()
    db.refresh(proveedor)
    return proveedor

@router.put("/prov/{prov_id}",response_model=page_schemas.proveedor)
def mod_prov(provid: int, entrada:page_schemas.proveedor_update,db:session=Depends(get_prov)):
    prov = db.query(page_models.proveedor).filter_by(id=provid).first()
    prov.nombreproveedor = entrada.nombreproveedor
    prov.procedencia = entrada.procedencia
    prov.telefono = entrada.telefono
    prov.correo = entrada.correo
    db.commit()
    db.refresh(prov)
    return prov

@router.delete("/prov/{prov_id}",response_model=page_schemas.respuesta)
def del_prov(provid: int,db:session=Depends(get_prov)):
    eliprov = db.query(page_models.proveedor).filter_by(id=provid).first()
    db.delete(eliprov)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta