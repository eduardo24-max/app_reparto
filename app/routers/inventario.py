from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/inventario", tags=["Inventario"])


@router.get("/", response_model=list[schemas.Inventario])
def listar_inventario(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_inventarios(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.Inventario)
def obtener_inventario(id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_inventario(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Registro de inventario no encontrado")
    return db_obj


@router.post("/", response_model=schemas.Inventario, status_code=201)
def crear_inventario(inventario: schemas.InventarioCreate, db: Session = Depends(get_db)):
    if not crud.get_producto(db, inventario.id_prod):
        raise HTTPException(status_code=400, detail="id_prod no existe en productos")
    return crud.create_inventario(db, inventario)


@router.put("/{id}", response_model=schemas.Inventario)
def actualizar_inventario(id: int, inventario: schemas.InventarioCreate, db: Session = Depends(get_db)):
    db_obj = crud.update_inventario(db, id, inventario)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Registro de inventario no encontrado")
    return db_obj


@router.delete("/{id}", status_code=204)
def eliminar_inventario(id: int, db: Session = Depends(get_db)):
    db_obj = crud.delete_inventario(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Registro de inventario no encontrado")
