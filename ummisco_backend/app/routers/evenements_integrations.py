from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import require_role
from app.models.models import Evenement, IntegrationExterne
from app.schemas.schemas import EvenementCreate, EvenementOut, IntegrationCreate, IntegrationOut

# ── Événements ────────────────────────────────────────────────

evenements_router = APIRouter(prefix="/evenements", tags=["Événements"])


@evenements_router.get("/", response_model=List[EvenementOut])
def list_evenements(
    skip: int = 0,
    limit: int = 20,
    axe_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Evenement)
    if axe_id:
        q = q.filter(Evenement.axe_id == axe_id)
    return q.order_by(Evenement.date_debut.desc()).offset(skip).limit(limit).all()


@evenements_router.post("/", response_model=EvenementOut, status_code=201)
def create_evenement(
    data: EvenementCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe", "chercheur")),
):
    evt = Evenement(**data.model_dump())
    db.add(evt)
    db.commit()
    db.refresh(evt)
    return evt


@evenements_router.get("/{evt_id}", response_model=EvenementOut)
def get_evenement(evt_id: int, db: Session = Depends(get_db)):
    evt = db.get(Evenement, evt_id)
    if not evt:
        raise HTTPException(status_code=404, detail="Événement introuvable")
    return evt


@evenements_router.patch("/{evt_id}", response_model=EvenementOut)
def update_evenement(
    evt_id: int,
    data: EvenementCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe")),
):
    evt = db.get(Evenement, evt_id)
    if not evt:
        raise HTTPException(status_code=404, detail="Événement introuvable")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(evt, field, value)
    db.commit()
    db.refresh(evt)
    return evt


@evenements_router.delete("/{evt_id}", status_code=204)
def delete_evenement(
    evt_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe")),
):
    evt = db.get(Evenement, evt_id)
    if not evt:
        raise HTTPException(status_code=404, detail="Événement introuvable")
    db.delete(evt)
    db.commit()


# ── Intégrations externes ─────────────────────────────────────

integrations_router = APIRouter(prefix="/integrations", tags=["Intégrations externes"])


@integrations_router.get("/", response_model=List[IntegrationOut])
def list_integrations(
    axe_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(IntegrationExterne).filter(IntegrationExterne.actif == True)
    if axe_id:
        q = q.filter(IntegrationExterne.axe_id == axe_id)
    return q.all()


@integrations_router.post("/", response_model=IntegrationOut, status_code=201)
def create_integration(
    data: IntegrationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("super_admin", "admin_axe", "chercheur", "doctorant")),
):
    role = current_user.role.libelle
    # Doctorant → intégration inactive jusqu'à validation par un chercheur/admin
    actif = role not in ("doctorant", "etudiant")
    ie = IntegrationExterne(**data.model_dump(), actif=actif)
    db.add(ie)
    db.commit()
    db.refresh(ie)
    return ie


@integrations_router.patch("/{ie_id}/toggle", response_model=IntegrationOut)
def toggle_integration(
    ie_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe", "chercheur")),
):
    ie = db.get(IntegrationExterne, ie_id)
    if not ie:
        raise HTTPException(status_code=404, detail="Intégration introuvable")
    ie.actif = not ie.actif
    db.commit()
    db.refresh(ie)
    return ie


@integrations_router.delete("/{ie_id}", status_code=204)
def delete_integration(
    ie_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe", "chercheur")),
):
    ie = db.get(IntegrationExterne, ie_id)
    if not ie:
        raise HTTPException(status_code=404, detail="Intégration introuvable")
    db.delete(ie)
    db.commit()
