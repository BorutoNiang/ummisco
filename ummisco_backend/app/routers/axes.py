from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models.models import AxeThematique, UtilisateurAxe
from app.schemas.schemas import AxeCreate, AxeUpdate, AxeOut

router = APIRouter(prefix="/axes", tags=["Axes thématiques"])


@router.get("/", response_model=List[AxeOut])
def list_axes(db: Session = Depends(get_db)):
    return db.query(AxeThematique).all()


@router.post("/", response_model=AxeOut, status_code=201)
def create_axe(
    data: AxeCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin")),
):
    axe = AxeThematique(**data.model_dump())
    db.add(axe)
    db.commit()
    db.refresh(axe)
    return axe


@router.get("/{axe_id}", response_model=AxeOut)
def get_axe(axe_id: int, db: Session = Depends(get_db)):
    axe = db.get(AxeThematique, axe_id)
    if not axe:
        raise HTTPException(status_code=404, detail="Axe introuvable")
    return axe


@router.patch("/{axe_id}", response_model=AxeOut)
def update_axe(
    axe_id: int,
    data: AxeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    axe = db.get(AxeThematique, axe_id)
    if not axe:
        raise HTTPException(status_code=404, detail="Axe introuvable")
    role = current_user.role.libelle
    # Responsable de l'axe ou super_admin peuvent modifier
    if axe.responsable_id != current_user.id and role != "super_admin":
        raise HTTPException(status_code=403, detail="Accès refusé")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(axe, field, value)
    db.commit()
    db.refresh(axe)
    return axe


@router.delete("/{axe_id}", status_code=204)
def delete_axe(
    axe_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin")),
):
    axe = db.get(AxeThematique, axe_id)
    if not axe:
        raise HTTPException(status_code=404, detail="Axe introuvable")
    db.delete(axe)
    db.commit()


# ── Membres de l'axe ──────────────────────────────────────────

@router.post("/{axe_id}/membres/{user_id}", status_code=201)
def add_membre(
    axe_id: int,
    user_id: int,
    role_axe: str = "membre",
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe")),
):
    existing = db.query(UtilisateurAxe).filter_by(utilisateur_id=user_id, axe_id=axe_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Utilisateur déjà membre de cet axe")
    ua = UtilisateurAxe(utilisateur_id=user_id, axe_id=axe_id, role_axe=role_axe)
    db.add(ua)
    db.commit()
    return {"message": "Membre ajouté"}


@router.delete("/{axe_id}/membres/{user_id}", status_code=204)
def remove_membre(
    axe_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe")),
):
    ua = db.query(UtilisateurAxe).filter_by(utilisateur_id=user_id, axe_id=axe_id).first()
    if not ua:
        raise HTTPException(status_code=404, detail="Membre introuvable")
    db.delete(ua)
    db.commit()
