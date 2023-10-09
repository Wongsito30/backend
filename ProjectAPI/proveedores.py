from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class proveedor(BaseModel):
    id: int
    nombre: str
    lugar: int
    telefono: str
    correo: float

proveedores = [proveedor(id="1",nombre="Levis", lugar="USA",telefono="6681234567", correo="levi@gmail.com")]

@app.get("/proveedorclass")
async def proveedorclass():
    return proveedores

def search_proveedor(id: id):
    proveer = filter(lambda proveedor: proveedor.idp == id, proveedor)
    try:
        return list(proveer)[0]
    except:
        return {"ERROR": "proveedor no encontrado"}

@app.post("/addproveedor/")
async def addproveedor(proveedor: proveedor):
    if type(search_proveedor(proveedor.id)) == proveedor:
        return {"ERROR": "Proveedor ya existe"}
    else:    
        proveedor.append(proveedor)

@app.put("/modproveedor/")
async def modproveedor(proveedor: proveedor):
    for index, savedproveer in enumerate(proveedores):
        if savedproveer.id == proveedor.id:
            proveedores[index] = proveedor
            return {"OK": "proveedor modificado"}
        

@app.delete("/delproveedor/{id}")
async def delproveerdor(id: int):
    for index, savedproveer in enumerate(proveedor):
        if savedproveer.id == id:
            del proveedores[index]
            return {"OK": "proveedor eliminado"}