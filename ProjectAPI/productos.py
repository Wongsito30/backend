from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class product(BaseModel):
    id: int
    nombre: str
    stock: int
    talla: str
    precio: float
    description: str
    imagen: str

products = [product(id="1",nombre="pantalon levi", stock="12",talla="M", precio="999.99", description="Color azul mezclilla", imagen="longblob")]

@app.get("/productclass")
async def productclass():
    return products

def search_product(id: id):
    product = filter(lambda product: product.id == id, products)
    try:
        return list(product)[0]
    except:
        return {"ERROR": "producto no encontrado"}

@app.post("/addproduct/")
async def addproduct(product: product):
    if type(search_product(product.id)) == product:
        return {"ERROR": "producto ya existe"}
    else:    
        products.append(product)

@app.put("/modproduct/")
async def modproduct(product: product):
    for index, savedproduct in enumerate(products):
        if savedproduct.id == product.id:
            products[index] = product
            return {"OK": "producto modificado"}
        

@app.delete("/delproduct/{id}")
async def delproduct(id: int):
    for index, savedproduct in enumerate(products):
        if savedproduct.id == id:
            del products[index]
            return {"OK": "producto eliminado"}