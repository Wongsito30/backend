from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class pago(BaseModel):
    id: int
    nombretarjeta: str
    numerotarjeta: int
    fecha: str
    cvv: int
    nickname: int
    

pagos = [pago(id="1",nombretarjeta="sahir Wong", numerotarjeta="1234123464567655", fecha="12/09/2023",cvv="121",nickname="Wongsito")]

@app.get("/pagoclass")
async def pagoclass():
    return pagos
    
def search_pago(id: id):
    pago = filter(lambda pago: pago.id == id, pagos)
    try:
        return list(pagos)[0]
    except:
        return {"ERROR": "metodo de pago no encontrado"}

@app.post("/addpago/")
async def addpago (pago: pago):
    if type(search_pago(pago.id)) == pago:
        return {"ERROR": "Metodo de pago ya existe"}
    else:    
        pagos.append(pagos)

@app.put("/modpago/")
async def modpago(pago: pago):
    for index, savedpago in enumerate(pago):
        if savedpago.id == pago.id:
            pagos[index] = pago
            return {"OK": "Metodo de pago modificado"}
        

@app.delete("/delpago/{id}")
async def delpago(id: int):
    for index, savedpago in enumerate(pagos):
        if savedpago.id == id:
            del pago[index]
            return {"OK": "Metodo de pago eliminado"}