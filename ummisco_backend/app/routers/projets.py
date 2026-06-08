from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models.models import Projet, ProjetPartenaire, ProjetMembre
from app.schemas.schemas import ProjetCreate, ProjetUpdate, ProjetOut

router = APIRouter(prefix="/projets", tags=["Projets"])


@router.get("/", response_model=List[ProjetOut])
def list_projets(
    skip: int = 0,
    limit: int = 20,
    axe_id: Optional[int] = None,
    statut: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Projet)
    if axe_id:
        q = q.filter(Projet.axe_id == axe_id)
    if statut:
        q = q.filter(Projet.statut == statut)
    return q.offset(skip).limit(limit).all()


@router.post("/", response_model=ProjetOut, status_code=201)
def create_projet(
    data: ProjetCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("super_admin", "admin_axe", "chercheur", "doctorant")),
):
    role = current_user.role.libelle
    # Doctorant → projet suspendu jusqu'à validation par un chercheur/admin
    if role in ("doctorant", "etudiant"):
        data = data.model_copy(update={"statut": "suspendu"})
    projet = Projet(**data.model_dump(), responsable_id=current_user.id)
    db.add(projet)
    db.commit()
    db.refresh(projet)
    return projet


@router.get("/{projet_id}", response_model=ProjetOut)
def get_projet(projet_id: int, db: Session = Depends(get_db)):
    projet = db.get(Projet, projet_id)
    if not projet:
        raise HTTPException(status_code=404, detail="Projet introuvable")
    return projet


@router.patch("/{projet_id}", response_model=ProjetOut)
def update_projet(
    projet_id: int,
    data: ProjetUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    projet = db.get(Projet, projet_id)
    if not projet:
        raise HTTPException(status_code=404, detail="Projet introuvable")
    if projet.responsable_id != current_user.id and current_user.role.libelle != "super_admin":
        raise HTTPException(status_code=403, detail="Accès refusé")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(projet, field, value)
    db.commit()
    db.refresh(projet)
    return projet


@router.delete("/{projet_id}", status_code=204)
def delete_projet(
    projet_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin")),
):
    projet = db.get(Projet, projet_id)
    if not projet:
        raise HTTPException(status_code=404, detail="Projet introuvable")
    db.delete(projet)
    db.commit()


# ── Partenaires du projet ─────────────────────────────────────

@router.post("/{projet_id}/partenaires/{partenaire_id}", status_code=201)
def add_partenaire(
    projet_id: int,
    partenaire_id: int,
    role_partenaire: str = "",
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe", "chercheur")),
):
    if db.query(ProjetPartenaire).filter_by(projet_id=projet_id, partenaire_id=partenaire_id).first():
        raise HTTPException(status_code=409, detail="Partenaire déjà lié au projet")
    pp = ProjetPartenaire(projet_id=projet_id, partenaire_id=partenaire_id, role_partenaire=role_partenaire)
    db.add(pp)
    db.commit()
    return {"message": "Partenaire ajouté"}


@router.delete("/{projet_id}/partenaires/{partenaire_id}", status_code=204)
def remove_partenaire(
    projet_id: int,
    partenaire_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe")),
):
    pp = db.query(ProjetPartenaire).filter_by(projet_id=projet_id, partenaire_id=partenaire_id).first()
    if not pp:
        raise HTTPException(status_code=404, detail="Association introuvable")
    db.delete(pp)
    db.commit()


# ── Membres du projet ─────────────────────────────────────────

@router.post("/{projet_id}/membres/{user_id}", status_code=201)
def add_membre_projet(
    projet_id: int,
    user_id: int,
    role_projet: str = "",
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe", "chercheur")),
):
    if db.query(ProjetMembre).filter_by(projet_id=projet_id, utilisateur_id=user_id).first():
        raise HTTPException(status_code=409, detail="Membre déjà dans le projet")
    pm = ProjetMembre(projet_id=projet_id, utilisateur_id=user_id, role_projet=role_projet)
    db.add(pm)
    db.commit()
    return {"message": "Membre ajouté au projet"}


@router.delete("/{projet_id}/membres/{user_id}", status_code=204)
def remove_membre_projet(
    projet_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe")),
):
    pm = db.query(ProjetMembre).filter_by(projet_id=projet_id, utilisateur_id=user_id).first()
    if not pm:
        raise HTTPException(status_code=404, detail="Membre introuvable dans le projet")
    db.delete(pm)
    db.commit()
