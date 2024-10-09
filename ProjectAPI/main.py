from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
from routers import loginadmin

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router, tags=["Login"])
app.include_router(loginadmin.app,tags=["Login admin"])
app.include_router(admins.router, tags=["Crud admin"])
app.include_router(carrito.router, tags=["Crud carrito"])
app.include_router(direccion.router, tags=["Crud direccion"])
app.include_router(historialcompra.router, tags=["Crud historial compras"])
app.include_router(pagos.router, tags=["Crud pagos"])
app.include_router(productos.router, tags=["Crud productos"])
app.include_router(proveedores.router, tags=["Crud proveedores"])
app.include_router(stock.router, tags=["Crud stock"])
app.include_router(sucursales.router, tags=["Crud sucursales"])
app.include_router(user.router, tags=["Crud usuarios"])
app.include_router(Wishlist.router, tags=["Crud wishlist"])
app.include_router(login.router, tags=["Login"])
app.include_router(loginadmin.app,tags=["Login admin"])
app.include_router(admins.router, tags=["Crud admin"])
app.include_router(carrito.router, tags=["Crud carrito"])
app.include_router(direccion.router, tags=["Crud direccion"])
app.include_router(historialcompra.router, tags=["Crud historial compras"])
app.include_router(pagos.router, tags=["Crud pagos"])
app.include_router(productos.router, tags=["Crud productos"])
app.include_router(proveedores.router, tags=["Crud proveedores"])
app.include_router(stock.router, tags=["Crud stock"])
app.include_router(sucursales.router, tags=["Crud sucursales"])
app.include_router(user.router, tags=["Crud usuarios"])
app.include_router(Wishlist.router, tags=["Crud wishlist"])

@app.get("/")
async def root():
    return {"message": "Hello World"}