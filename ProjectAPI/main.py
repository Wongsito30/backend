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
app.include_router(loginadmin.app)


@app.get("/")
async def root():
    return {"message": "Hello World"}