from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class direccion(BaseModel):
    id: int
    nombrecalle: str
    numerocasa: int
    cp: int
    colonia: float
    estado: str
    municipio: str

direcciones = [direccion(id="1",nombrecalle="Lomas", numerocasa="123",cp="81234", colonia="Teresa", estado="Sinaloa", municipio="Guasave")]

@app.get("/direccionclass")
async def direccionclass():
    return direcciones

def search_direccion(id: id):
    direccion = filter(lambda direccion: direccion.id == id, direccion)
    try:
        return list(direcciones)[0]
    except:
        return {"ERROR": "direccion no encontrada"}

@app.post("/adddireccion/")
async def adddireccion(direccion: direccion):
    if type(search_direccion(direccion.id)) == direccion:
        return {"ERROR": "direccion ya existe"}
    else:    
        direcciones.append(direccion)

@app.put("/moddireccion/")
async def moddireccion(direccion: direccion):
    for index, saveddireccion in enumerate(direcciones):
        if saveddireccion.id == direccion.id:
            direcciones[index] = direccion
            return {"OK": "direccion modificada"}
        

@app.delete("/deldireccion/{id}")
async def deldireccion(id: int):
    for index, saveddireccion in enumerate(direcciones):
        if saveddireccion.id == id:
            del direcciones[index]
            return {"OK": "direccion eliminada"}