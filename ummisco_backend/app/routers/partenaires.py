from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import require_role
from app.models.models import Partenaire
from app.schemas.schemas import PartenaireCreate, PartenaireOut

router = APIRouter(prefix="/partenaires", tags=["Partenaires"])


@router.get("/", response_model=List[PartenaireOut])
def list_partenaires(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Partenaire).offset(skip).limit(limit).all()


@router.post("/", response_model=PartenaireOut, status_code=201)
def create_partenaire(
    data: PartenaireCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe")),
):
    p = Partenaire(**data.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@router.get("/{p_id}", response_model=PartenaireOut)
def get_partenaire(p_id: int, db: Session = Depends(get_db)):
    p = db.get(Partenaire, p_id)
    if not p:
        raise HTTPException(status_code=404, detail="Partenaire introuvable")
    return p


@router.patch("/{p_id}", response_model=PartenaireOut)
def update_partenaire(
    p_id: int,
    data: PartenaireCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe")),
):
    p = db.get(Partenaire, p_id)
    if not p:
        raise HTTPException(status_code=404, detail="Partenaire introuvable")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(p, field, value)
    db.commit()
    db.refresh(p)
    return p


@router.delete("/{p_id}", status_code=204)
def delete_partenaire(
    p_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin")),
):
    p = db.get(Partenaire, p_id)
    if not p:
        raise HTTPException(status_code=404, detail="Partenaire introuvable")
    db.delete(p)
    db.commit()
