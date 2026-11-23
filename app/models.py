from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Producto(Base):
    __tablename__ = "productos"

    id_prod = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)

    platillos = relationship("Platillo", back_populates="producto", cascade="all, delete-orphan")
    inventario = relationship("Inventario", back_populates="producto")


class Trabajador(Base):
    __tablename__ = "trabajadores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    puesto = Column(String(50), nullable=True)

    platillos = relationship("Platillo", back_populates="trabajador")


class Platillo(Base):
    __tablename__ = "platillos"

    id_plat = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)

    id_prod = Column(Integer, ForeignKey("productos.id_prod"), nullable=False)
    id_trabajador = Column(Integer, ForeignKey("trabajadores.id"), nullable=True)

    producto = relationship("Producto", back_populates="platillos")
    trabajador = relationship("Trabajador", back_populates="platillos")


class Inventario(Base):
    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True, index=True)
    id_prod = Column(Integer, ForeignKey("productos.id_prod"), nullable=False)
    cantidad = Column(Integer, nullable=False, default=0)

    producto = relationship("Producto", back_populates="inventario")
