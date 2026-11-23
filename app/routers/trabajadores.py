from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/trabajadores", tags=["Trabajadores"])


@router.get("/", response_model=list[schemas.Trabajador])
def listar_trabajadores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_trabajadores(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.Trabajador)
def obtener_trabajador(id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_trabajador(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    return db_obj


@router.post("/", response_model=schemas.Trabajador, status_code=201)
def crear_trabajador(trabajador: schemas.TrabajadorCreate, db: Session = Depends(get_db)):
    return crud.create_trabajador(db, trabajador)


@router.put("/{id}", response_model=schemas.Trabajador)
def actualizar_trabajador(id: int, trabajador: schemas.TrabajadorCreate, db: Session = Depends(get_db)):
    db_obj = crud.update_trabajador(db, id, trabajador)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    return db_obj


@router.delete("/{id}", status_code=204)
def eliminar_trabajador(id: int, db: Session = Depends(get_db)):
    db_obj = crud.delete_trabajador(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
