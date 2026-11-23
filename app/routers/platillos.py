from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/platillos", tags=["Platillos"])


@router.get("/", response_model=list[schemas.Platillo])
def listar_platillos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_platillos(db, skip=skip, limit=limit)


@router.get("/{id_plat}", response_model=schemas.Platillo)
def obtener_platillo(id_plat: int, db: Session = Depends(get_db)):
    db_obj = crud.get_platillo(db, id_plat)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Platillo no encontrado")
    return db_obj


@router.post("/", response_model=schemas.Platillo, status_code=201)
def crear_platillo(platillo: schemas.PlatilloCreate, db: Session = Depends(get_db)):
    # valida que el producto exista
    if not crud.get_producto(db, platillo.id_prod):
        raise HTTPException(status_code=400, detail="id_prod no existe en productos")
    if platillo.id_trabajador is not None and not crud.get_trabajador(db, platillo.id_trabajador):
        raise HTTPException(status_code=400, detail="id_trabajador no existe en trabajadores")
    return crud.create_platillo(db, platillo)


@router.put("/{id_plat}", response_model=schemas.Platillo)
def actualizar_platillo(id_plat: int, platillo: schemas.PlatilloCreate, db: Session = Depends(get_db)):
    db_obj = crud.update_platillo(db, id_plat, platillo)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Platillo no encontrado")
    return db_obj


@router.delete("/{id_plat}", status_code=204)
def eliminar_platillo(id_plat: int, db: Session = Depends(get_db)):
    db_obj = crud.delete_platillo(db, id_plat)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Platillo no encontrado")
