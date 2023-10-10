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


def get_pagos():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@app.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@app.get("/pagos/", response_model=List[page_schemas.pagos])
async def show_pagos(db:session=Depends(get_pagos)):
    pay = db.query(page_models.pagos).all()
    return pay

@app.post("/pagos/",response_model=page_schemas.pagos)
def create_pagos(entrada:page_schemas.pagos,db:session=Depends(get_pagos)):
    pay = page_models.pagos(nombretarjeta = entrada.nombretarjeta,numerotarjeta = entrada.numerotarjeta, fecha = entrada.fecha, cvv = entrada.cvv, nickname = entrada.nickname)
    db.add(pay)
    db.commit()
    db.refresh(pay)
    return pay

@app.put("/pagos/{pagos_id}",response_model=page_schemas.pagos)
def mod_pagos(pagosid: int, entrada:page_schemas.pagos_update,db:session=Depends(get_pagos)):
    pay = db.query(page_models.pagos).filter_by(id=pagosid).first()
    pay.nombretarjeta = entrada.nombretarjeta
    pay.numerotarjeta = entrada.numerotarjeta
    pay.fecha = entrada.fecha
    pay.cvv = entrada.cvv
    pay.nickname = entrada.nickname
    db.commit()
    db.refresh(pay)
    return pay

@app.delete("/pagos/{pagos_id}",response_model=page_schemas.respuesta)
def del_pagos(pagosid: int,db:session=Depends(get_pagos)):
    elipagos = db.query(page_models.pagos).filter_by(id=pagosid).first()
    db.delete(elipagos)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta