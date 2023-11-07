from fastapi import FastAPI
from typing import List
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from fastapi.params import Depends
from passlib.context import CryptContext

from BD.conexion import engine, sessionlocal

import BD.schemas as page_schemas
import BD.conexion as page_conexion
import BD.models as page_models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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

@app.get("/searchusercorreo/{Correo}", response_model=List[page_schemas.User])
async def show_pass_correo(correo: str, db: session = Depends(get_user)):
    passs = db.query(page_models.User).filter(page_models.User.email == correo).first()
    user = [passs.contrasena]
    return [user]

@app.post("/users/",response_model=page_schemas.User)
def create_user(entrada:page_schemas.User,db:session=Depends(get_user)):
    hashed_password = pwd_context.hash(entrada.contrasena)
    usuario = page_models.User(nickname = entrada.nickname,contrasena = hashed_password, email = entrada.email, estado = entrada.estado)
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

@app.put("/contrasena/{contra_id}",response_model=page_schemas.User)
def mod_contra(contraid: int, entrada:page_schemas.contrasena_update,db:session=Depends(get_user)):
    usuario = db.query(page_models.User).filter_by(id=contraid).first()
    usuario.contrasena = entrada.contrasena
    db.commit()
    db.refresh(usuario)
    return usuario

@app.put("/email/{email_id}",response_model=page_schemas.User)
def mod_email(emailid: int, entrada:page_schemas.email_update,db:session=Depends(get_user)):
    usuario = db.query(page_models.User).filter_by(id=emailid).first()
    usuario.email = entrada.email
    db.commit()
    db.refresh(usuario)
    return usuario

@app.put("/usersadmin/{usuario_id}",response_model=page_schemas.User)
def mod_user_admin(usuarioid: int, entrada:page_schemas.User_update_admin,db:session=Depends(get_user)):
    usuario = db.query(page_models.User).filter_by(id=usuarioid).first()
    usuario.nickname = entrada.nickname
    usuario.contrasena = entrada.contrasena
    usuario.email = entrada.email
    usuario.estado = entrada.estado
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

