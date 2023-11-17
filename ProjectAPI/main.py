from fastapi import FastAPI
from routers import admins
from routers import carrito
from routers import direccion
from routers import historialcompra
from routers import login
from routers import pagos
from routers import productos
from routers import proveedores
from routers import stock
from routers import sucursales
from routers import user
from routers import Wishlist

app = FastAPI()
#router
app.include_router(admins.router)
app.include_router(carrito.router)
app.include_router(direccion.router)
app.include_router(historialcompra.router)
app.include_router(login.router)
app.include_router(pagos.router)
app.include_router(productos.router)
app.include_router(proveedores.router)
app.include_router(stock.router)
app.include_router(sucursales.router)
app.include_router(user.router)
app.include_router(Wishlist.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}