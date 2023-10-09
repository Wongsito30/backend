from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class product(BaseModel):
    id: int
    nickname: str
    nombre: str
    stock: int
    talla: str
    cantidad: int
    precio: float
    

products = [product(id="1",nickname="sahir",nombre="pantalon levi", stock="12",cantidad="12",talla="G", precio="999.99")]

@app.get("/cartclass")
async def cartclass():
    return products

@app.get("/usercart/")
async def usercart(nickname: str):
    usuario = filter(lambda product: product.nickname == nickname, product)
    try:
        return list(usuario)[0]
    except:
        return {"ERROR": "usuario no encontrado"}
    
def search_cart(id: id):
    usuario = filter(lambda product: product.id == id, products)
    try:
        return list(usuario)[0]
    except:
        return {"ERROR": "producto no encontrado"}

@app.post("/addcart/")
async def addcart (product: product):
    if type(search_cart(product.id)) == product:
        return {"ERROR": "usuario ya existe"}
    else:    
        products.append(product)

@app.put("/modcart/")
async def modcart(product: product):
    for index, savedproduct in enumerate(products):
        if savedproduct.id == product.id:
            products[index] = product
            return {"OK": "producto modificado"}
        

@app.delete("/delcart/{id}")
async def delcart(id: int):
    for index, savedproduct in enumerate(products):
        if savedproduct.id == id:
            del products[index]
            return {"OK": "producto eliminado"}