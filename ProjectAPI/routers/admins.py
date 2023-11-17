from fastapi import APIRouter ,HTTPException
from typing import List
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from sqlalchemy import func
from fastapi.params import Depends
from passlib.context import CryptContext
from BD.conexion import engine, sessionlocal

import BD.schemas as page_schemas
import BD.conexion as page_conexion
import BD.models as page_models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
page_models.Base.metadata.create_all(bind=engine)
router = APIRouter()


def get_admin():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()


@router.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@router.get("/admins/", response_model=List[page_schemas.Admin])
async def show_admin(db:session=Depends(get_admin)):
    admin = db.query(page_models.Admin).all()
    return admin


@router.post("/admins/",response_model=page_schemas.Admin)
def create_admin(entrada:page_schemas.Admin,db:session=Depends(get_admin)):
    hashed_password = pwd_context.hash(entrada.contrasena)
    max_id = db.query(func.max(page_models.Admin.id)).scalar() or 0
    # Incrementar la ID para el nuevo administrador
    new_id = max_id + 1
    admin = "admin" + str(new_id)
    admin  = page_models.Admin(admin = admin,contrasena = hashed_password, estado = entrada.estado)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


@router.put("/admincontrasena/{id}",response_model=page_schemas.Admin)
def mod_contraadmin(id: int, entrada:page_schemas.contrasena_update,db:session=Depends(get_admin)):
    admin = db.query(page_models.Admin).filter_by(id=id).first()
    hashed_password = pwd_context.hash(entrada.contrasena)
    admin.contrasena = hashed_password
    db.commit()
    db.refresh(admin)
    return admin

@router.delete("/admin/{admin_id}",response_model=page_schemas.respuesta)
def del_admin(adminid: int,db:session=Depends(get_admin)):
    admin = db.query(page_models.Admin).filter_by(id=adminid).first()
    db.delete(admin)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta