from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import hash_password, require_role, get_current_user
from app.models.models import Utilisateur
from app.schemas.schemas import UtilisateurCreate, UtilisateurUpdate, UtilisateurOut

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])


@router.get("/", response_model=List[UtilisateurOut])
def list_utilisateurs(
    skip: int = 0, limit: int = 20,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe")),
):
    return db.query(Utilisateur).offset(skip).limit(limit).all()


@router.post("/", response_model=UtilisateurOut, status_code=201)
def create_utilisateur(
    data: UtilisateurCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin")),
):
    if db.query(Utilisateur).filter(Utilisateur.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email déjà utilisé")
    user = Utilisateur(
        nom=data.nom,
        prenom=data.prenom,
        email=data.email,
        password_hash=hash_password(data.password),
        role_id=data.role_id,
        langue=data.langue,
        bio=data.bio,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UtilisateurOut)
def get_utilisateur(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Un utilisateur peut voir son propre profil, un admin peut voir tous
    if current_user.id != user_id and current_user.role.libelle not in ("super_admin", "admin_axe"):
        raise HTTPException(status_code=403, detail="Accès refusé")
    user = db.get(Utilisateur, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user


@router.patch("/{user_id}", response_model=UtilisateurOut)
def update_utilisateur(
    user_id: int,
    data: UtilisateurUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id and current_user.role.libelle != "super_admin":
        raise HTTPException(status_code=403, detail="Accès refusé")
    user = db.get(Utilisateur, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204)
def delete_utilisateur(
    user_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin")),
):
    user = db.get(Utilisateur, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    db.delete(user)
    db.commit()
