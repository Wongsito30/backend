from fastapi import FastAPI, HTTPException
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


def get_his():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@app.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@app.get("/his/", response_model=List[page_schemas.Historial])
async def show_his(db:session=Depends(get_his)):
    historial = db.query(page_models.Historial).all()
    return historial

@app.get("/searchhis/{hisname}", response_model=List[page_schemas.Historial])
async def show_his_user(hisname: str, db: session = Depends(get_his)):
    # Filtra los productos que coinciden con el nombre
    historial = db.query(page_models.Historial).filter(page_models.Car.nickname == hisname).all()
    
    if not historial:
        raise HTTPException(status_code=404, detail=f"No se encontro historial para el usuario {hisname}")


    return historial

@app.post("/his/",response_model=page_schemas.Historial)
def create_his(entrada:page_schemas.Historial,db:session=Depends(get_his)):
    historial = page_models.Historial(nombreproducto = entrada.nombreproducto, talla = entrada.talla, cantidad = entrada.cantidad, preciototal = entrada.preciototal, nickname = entrada.nickname, categoria = entrada.categoria, nombreproveedor = entrada.nombreproveedor, nombresucursal = entrada.nombresucursal)
    db.add(historial)
    db.commit()
    db.refresh(historial)
    return historial

@app.put("/his/{his_id}",response_model=page_schemas.Historial)
def mod_his(hisid: int, entrada:page_schemas.historial_update,db:session=Depends(get_his)):
    his = db.query(page_models.Historial).filter_by(id=hisid).first()
    his.nombreproducto = entrada.nombreproducto
    his.talla = entrada.talla
    his.cantidad = entrada.cantidad
    his.preciototal = entrada.preciototal
    his.nickname = entrada.nickname
    his.categoria = entrada.categoria
    his.nombreproveedor = entrada.nombreproveedor
    his.nombresucursal = entrada.nombresucursal
    db.commit()
    db.refresh(his)
    return his

@app.delete("/his/{his_id}",response_model=page_schemas.respuesta)
def del_his(hisid: int,db:session=Depends(get_his)):
    elihis = db.query(page_models.Historial).filter_by(id=hisid).first()
    db.delete(elihis)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta