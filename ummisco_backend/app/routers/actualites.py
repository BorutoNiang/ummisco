from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models.models import Actualite, Utilisateur
from app.schemas.schemas import ActualiteCreate, ActualiteOut, ValidationRequest

router = APIRouter(prefix="/actualites", tags=["Actualités"])


@router.get("/", response_model=List[ActualiteOut])
def list_actualites(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return (
        db.query(Actualite)
        .filter(Actualite.statut == "publie")
        .order_by(Actualite.date_publication.desc())
        .offset(skip).limit(limit).all()
    )


@router.post("/", response_model=ActualiteOut, status_code=201)
def create_actualite(
    data: ActualiteCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    role = current_user.role.libelle
    # Chercheur/admin → publication directe. Doctorant/autres → validation requise.
    if role in ("chercheur", "super_admin", "admin_axe"):
        statut   = "publie"
        date_pub = datetime.now(timezone.utc)
    else:
        statut   = "en_attente"
        date_pub = None

    actu = Actualite(
        **data.model_dump(),
        auteur_id=current_user.id,
        statut=statut,
        date_publication=date_pub,
    )
    db.add(actu)
    db.commit()
    db.refresh(actu)
    return actu


@router.get("/en-attente", response_model=List[ActualiteOut])
def list_en_attente(
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe")),
):
    return db.query(Actualite).filter(Actualite.statut == "en_attente").all()


@router.get("/{actu_id}", response_model=ActualiteOut)
def get_actualite(actu_id: int, db: Session = Depends(get_db)):
    actu = db.get(Actualite, actu_id)
    if not actu or actu.statut != "publie":
        raise HTTPException(status_code=404, detail="Actualité introuvable")
    return actu


@router.post("/{actu_id}/valider", response_model=ActualiteOut)
def valider_actualite(
    actu_id: int,
    data: ValidationRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("super_admin", "admin_axe", "chercheur")),
):
    actu = db.get(Actualite, actu_id)
    if not actu:
        raise HTTPException(status_code=404, detail="Actualité introuvable")
    if actu.statut != "en_attente":
        raise HTTPException(status_code=400, detail="Actualité non en attente de validation")

    if data.decision == "approuver":
        actu.statut = "publie"
        actu.date_publication = datetime.now(timezone.utc)
    elif data.decision == "rejeter":
        actu.statut = "rejete"
    else:
        raise HTTPException(status_code=400, detail="Décision invalide")

    actu.validateur_id = current_user.id
    db.commit()
    db.refresh(actu)
    return actu


@router.patch("/{actu_id}", response_model=ActualiteOut)
def update_actualite(
    actu_id: int,
    data: ActualiteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    actu = db.get(Actualite, actu_id)
    if not actu:
        raise HTTPException(status_code=404, detail="Actualité introuvable")
    if actu.auteur_id != current_user.id and current_user.role.libelle != "super_admin":
        raise HTTPException(status_code=403, detail="Accès refusé")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(actu, field, value)
    db.commit()
    db.refresh(actu)
    return actu


@router.delete("/{actu_id}", status_code=204)
def delete_actualite(
    actu_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    actu = db.get(Actualite, actu_id)
    if not actu:
        raise HTTPException(status_code=404, detail="Actualité introuvable")
    if actu.auteur_id != current_user.id and current_user.role.libelle != "super_admin":
        raise HTTPException(status_code=403, detail="Accès refusé")
    db.delete(actu)
    db.commit()
