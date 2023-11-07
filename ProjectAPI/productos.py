from fastapi import FastAPI, Query
from typing import List
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from sqlalchemy import create_engine, asc, desc, func
from fastapi.params import Depends
from BD.conexion import engine, sessionlocal
import BD.schemas as page_schemas
import BD.conexion as page_conexion
import BD.models as page_models

page_models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_product():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@app.get("/")
async def Main():
    return RedirectResponse(url="/docs/")

@app.get("/products/", response_model=List[page_schemas.Product])
async def show_products(db:session=Depends(get_product)):
    productos = db.query(page_models.Products).all()
    return productos

@app.get("/searchcate/{catename}", response_model=List[page_schemas.Product])
async def show_cat_user(catname: str, db: session = Depends(get_product)):
    # Filtra los productos que coinciden con el nombre
    categoria = db.query(page_models.Products).filter(page_models.Products.categoria == catname).all()
    return categoria

@app.get("/searchproducts/{productname}", response_model=List[page_schemas.Product])
async def show_product(productname: str, db: session = Depends(get_product)):
    # Filtra los productos que coinciden con el nombre
    products = db.query(page_models.Products).filter(func.lower(page_models.Products.nombreproducto).ilike(f"%{productname}%")).all()
    return products

@app.get("/searchproductsprov/{proveedorname}", response_model=List[page_schemas.Product])
async def show_product_prov(proveedorname: str, db: session = Depends(get_product)):
    # Filtra los productos que coinciden con el nombre
    products = db.query(page_models.Products).filter(func.lower(page_models.Products.nombreproveedor).ilike(f"%{proveedorname}%")).all()
    return products

@app.get("/searchproductssuc/{sucursalname}", response_model=List[page_schemas.Product])
async def show_product_suc(sucursalname: str, db: session = Depends(get_product)):
    # Filtra los productos que coinciden con el nombre
    products = db.query(page_models.Products).filter(func.lower(page_models.Products.nombresucursal).ilike(f"%{sucursalname}%")).all()
    return products

@app.get("/products/precioasc", response_model=List[page_schemas.Product])
async def get_products_ascending(
    db: session = Depends(get_product),
    field: str = Query("precio")
):
    if field not in page_models.Products.__table__.columns:
        return {"error": "Campo no válido"}

    # Ordena de menor a mayor
    products = db.query(page_models.Products).order_by(asc(field)).all()
    return products

@app.get("/products/stockasc", response_model=List[page_schemas.Product])
async def get_products_ascending(
    db: session = Depends(get_product),
    field: str = Query("stock")
):
    if field not in page_models.Products.__table__.columns:
        return {"error": "Campo no válido"}

    # Ordena de menor a mayor
    products = db.query(page_models.Products).order_by(asc(field)).all()
    return products

@app.get("/products/preciodesc", response_model=List[page_schemas.Product])
async def get_products_descending(
    db: session = Depends(get_product),
    field: str = Query("precio")
):
    if field not in page_models.Products.__table__.columns:
        return {"error": "Campo no válido"}
    # Ordena de mayor a menor
    products = db.query(page_models.Products).order_by(desc(field)).all()
    return products

@app.get("/products/stockdesc", response_model=List[page_schemas.Product])
async def get_products_descending(
    db: session = Depends(get_product),
    field: str = Query("stock")
):
    if field not in page_models.Products.__table__.columns:
        return {"error": "Campo no válido"}
    # Ordena de mayor a menor
    products = db.query(page_models.Products).order_by(desc(field)).all()
    return products

@app.post("/products/",response_model=page_schemas.Product)
def create_product(entrada:page_schemas.Product,db:session=Depends(get_product)):
    producto = page_models.Products(nombreproducto = entrada.nombreproducto,stock = entrada.stock, talla = entrada.talla, precio = entrada.precio, descripcion = entrada.descripcion, imagen = entrada.imagen, categoria = entrada.categoria,nombreproveedor = entrada.nombreproveedor,nombresucursal = entrada.nombresucursal)
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto

@app.put("/products/{producto_id}",response_model=page_schemas.Product)
def mod_product(productoid: int, entrada:page_schemas.product_update,db:session=Depends(get_product)):
    producto = db.query(page_models.Products).filter_by(id=productoid).first()
    producto.nombreproducto = entrada.nombreproducto
    producto.stock = entrada.stock
    producto.talla = entrada.talla
    producto.precio = entrada.precio
    producto.descripcion = entrada.descripcion
    producto.imagen = entrada.imagen
    producto.categoria = entrada.categoria
    producto.nombreproveedor = entrada.nombreproveedor
    producto.nombresucursal = entrada.nombresucursal
    db.commit()
    db.refresh(producto)
    return producto

@app.delete("/products/{producto_id}",response_model=page_schemas.respuesta)
def del_product(productoid: int,db:session=Depends(get_product)):
    eliproducto = db.query(page_models.Products).filter_by(id=productoid).first()
    db.delete(eliproducto)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta