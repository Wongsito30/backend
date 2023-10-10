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


def get_user():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@app.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@app.get("/users/", response_model=List[page_schemas.User])
async def show_users(db:session=Depends(get_user)):
    usuarios = db.query(page_models.User).all()
    return usuarios

@app.post("/users/",response_model=page_schemas.User)
def create_user(entrada:page_schemas.User,db:session=Depends(get_user)):
    usuario = page_models.User(nickname = entrada.nickname,contrasena = entrada.contrasena, email = entrada.email, estado = entrada.estado)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@app.put("/users/{usuario_id}",response_model=page_schemas.User)
def mod_user(usuarioid: int, entrada:page_schemas.User_update,db:session=Depends(get_user)):
    usuario = db.query(page_models.User).filter_by(id=usuarioid).first()
    usuario.nickname = entrada.nickname
    db.commit()
    db.refresh(usuario)
    return usuario

@app.delete("/users/{usuario_id}",response_model=page_schemas.respuesta)
def del_user(usuarioid: int,db:session=Depends(get_user)):
    usuario = db.query(page_models.User).filter_by(id=usuarioid).first()
    db.delete(usuario)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta

