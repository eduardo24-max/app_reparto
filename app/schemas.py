from typing import Optional
from pydantic import BaseModel, ConfigDict


# ---------- Producto ----------
class ProductoBase(BaseModel):
    nombre: str
    precio: float


class ProductoCreate(ProductoBase):
    pass


class Producto(ProductoBase):
    model_config = ConfigDict(from_attributes=True)
    id_prod: int


# ---------- Trabajador ----------
class TrabajadorBase(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    puesto: Optional[str] = None


class TrabajadorCreate(TrabajadorBase):
    pass


class Trabajador(TrabajadorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------- Platillo ----------
class PlatilloBase(BaseModel):
    nombre: str
    precio: float
    id_prod: int
    id_trabajador: Optional[int] = None


class PlatilloCreate(PlatilloBase):
    pass


class Platillo(PlatilloBase):
    model_config = ConfigDict(from_attributes=True)
    id_plat: int


# ---------- Inventario ----------
class InventarioBase(BaseModel):
    id_prod: int
    cantidad: int


class InventarioCreate(InventarioBase):
    pass


class Inventario(InventarioBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
