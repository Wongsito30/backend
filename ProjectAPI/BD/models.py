from sqlalchemy import Column, Integer, String, LargeBinary, Float, Date
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50))
    contrasena =  Column(String(16))
    email = Column(String(255))
    estado = Column(Integer)

class Products(Base):
    __tablename__ = 'Productos'

    id = Column(Integer, primary_key=True, index=True)
    nombreproducto = Column(String(50))
    stock =  Column(Integer)
    talla = Column(String(10))
    precio = Column(Float)
    descripcion = Column(String(250))
    imagen = Column(LargeBinary)

class Car(Base):
    __tablename__ = 'carrito'

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50))
    nombreproducto = Column(String(50))
    stock =  Column(Integer)
    talla = Column(String(10))
    cantidad = Column(Integer)
    preciototal = Column(Float)
    imagen = Column(LargeBinary)

class Wishlist(Base):
    __tablename__ = 'favoritos'

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50))
    nombreproducto = Column(String(50))
    stock =  Column(Integer)
    talla = Column(String(10))
    cantidad = Column(Integer)
    imagen = Column(LargeBinary)

class Direction(Base):
    __tablename__ = 'direccion'

    id = Column(Integer, primary_key=True, index=True)
    nombrecalle = Column(String(100))
    numerocasa = Column(Integer)
    cp =  Column(Integer)
    colonia = Column(String(100))
    estado = Column(String(100))
    municipio = Column(String(100))
    nickname = Column(String(50))

class pagos(Base):
    __tablename__ = 'pagos'

    id = Column(Integer, primary_key=True, index=True)
    nombretarjeta = Column(String(200))
    numerotarjeta = Column(String(16))
    fecha =  Column(Date)
    cvv = Column(Integer)
    nickname = Column(String(50))

class proveedor(Base):
    __tablename__ = 'proveedores'

    id = Column(Integer, primary_key=True, index=True)
    nombreproveedor = Column(String(200))
    procedencia = Column(String(100))
    telefono =  Column(String(10))
    correo = Column(String(150))