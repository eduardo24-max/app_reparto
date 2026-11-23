from sqlalchemy.orm import Session

from . import models, schemas


# ---------- Producto ----------
def get_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Producto).offset(skip).limit(limit).all()


def get_producto(db: Session, id_prod: int):
    return db.query(models.Producto).filter(models.Producto.id_prod == id_prod).first()


def create_producto(db: Session, producto: schemas.ProductoCreate):
    db_obj = models.Producto(**producto.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_producto(db: Session, id_prod: int, cambios: schemas.ProductoCreate):
    db_obj = get_producto(db, id_prod)
    if not db_obj:
        return None
    for campo, valor in cambios.model_dump().items():
        setattr(db_obj, campo, valor)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_producto(db: Session, id_prod: int):
    db_obj = get_producto(db, id_prod)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj


# ---------- Trabajador ----------
def get_trabajadores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Trabajador).offset(skip).limit(limit).all()


def get_trabajador(db: Session, id: int):
    return db.query(models.Trabajador).filter(models.Trabajador.id == id).first()


def create_trabajador(db: Session, trabajador: schemas.TrabajadorCreate):
    db_obj = models.Trabajador(**trabajador.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_trabajador(db: Session, id: int, cambios: schemas.TrabajadorCreate):
    db_obj = get_trabajador(db, id)
    if not db_obj:
        return None
    for campo, valor in cambios.model_dump().items():
        setattr(db_obj, campo, valor)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_trabajador(db: Session, id: int):
    db_obj = get_trabajador(db, id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj


# ---------- Platillo ----------
def get_platillos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Platillo).offset(skip).limit(limit).all()


def get_platillo(db: Session, id_plat: int):
    return db.query(models.Platillo).filter(models.Platillo.id_plat == id_plat).first()


def create_platillo(db: Session, platillo: schemas.PlatilloCreate):
    db_obj = models.Platillo(**platillo.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_platillo(db: Session, id_plat: int, cambios: schemas.PlatilloCreate):
    db_obj = get_platillo(db, id_plat)
    if not db_obj:
        return None
    for campo, valor in cambios.model_dump().items():
        setattr(db_obj, campo, valor)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_platillo(db: Session, id_plat: int):
    db_obj = get_platillo(db, id_plat)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj


# ---------- Inventario ----------
def get_inventarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Inventario).offset(skip).limit(limit).all()


def get_inventario(db: Session, id: int):
    return db.query(models.Inventario).filter(models.Inventario.id == id).first()


def create_inventario(db: Session, inventario: schemas.InventarioCreate):
    db_obj = models.Inventario(**inventario.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_inventario(db: Session, id: int, cambios: schemas.InventarioCreate):
    db_obj = get_inventario(db, id)
    if not db_obj:
        return None
    for campo, valor in cambios.model_dump().items():
        setattr(db_obj, campo, valor)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_inventario(db: Session, id: int):
    db_obj = get_inventario(db, id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj
