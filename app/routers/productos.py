from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/", response_model=list[schemas.Producto])
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_productos(db, skip=skip, limit=limit)


@router.get("/{id_prod}", response_model=schemas.Producto)
def obtener_producto(id_prod: int, db: Session = Depends(get_db)):
    db_obj = crud.get_producto(db, id_prod)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_obj


@router.post("/", response_model=schemas.Producto, status_code=201)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.create_producto(db, producto)


@router.put("/{id_prod}", response_model=schemas.Producto)
def actualizar_producto(id_prod: int, producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    db_obj = crud.update_producto(db, id_prod, producto)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_obj


@router.delete("/{id_prod}", status_code=204)
def eliminar_producto(id_prod: int, db: Session = Depends(get_db)):
    db_obj = crud.delete_producto(db, id_prod)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
