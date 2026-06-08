from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timezone
from typing import List, Optional
import os, shutil, uuid

from app.core.database import get_db
from app.core.security import get_current_user, get_current_user_optional, require_role
from app.core.config import settings
from app.models.models import Publication, Utilisateur
from app.schemas.schemas import (
    PublicationCreate, PublicationUpdate, PublicationOut, ValidationRequest
)

router = APIRouter(prefix="/publications", tags=["Publications"])


def _can_see(pub: Publication, user: Optional[Utilisateur]) -> bool:
    """Vérifie si l'utilisateur peut voir cette publication selon la visibilité."""
    if pub.visibilite == "public":
        return True
    if not user:
        return False
    if pub.visibilite == "prive":
        return pub.auteur_id == user.id
    # protege → membres UMMISCO (tout rôle sauf visiteur)
    return user.role.libelle != "visiteur"


@router.get("/", response_model=List[PublicationOut])
def list_publications(
    skip: int = 0,
    limit: int = 20,
    axe_id: Optional[int] = None,
    statut: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[Utilisateur] = Depends(get_current_user_optional),
):
    q = db.query(Publication)
    if axe_id:
        q = q.filter(Publication.axe_id == axe_id)
    if statut:
        q = q.filter(Publication.statut == statut)
    else:
        q = q.filter(Publication.statut == "publie")
    pubs = q.offset(skip).limit(limit).all()
    return [p for p in pubs if _can_see(p, current_user)]


@router.post("/", response_model=PublicationOut, status_code=201)
def create_publication(
    data: PublicationCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    role = current_user.role.libelle

    # Workflow de validation :
    # - super_admin / admin_axe / chercheur → publication directe
    # - doctorant / étudiant / autres → en_attente, validation obligatoire
    # Note : peer_reviewed ne donne PAS accès direct pour les doctorants,
    #        c'est juste un attribut documentaire.
    roles_publication_directe = ("chercheur", "super_admin", "admin_axe")

    if role in roles_publication_directe:
        statut   = "publie"
        date_pub = datetime.now(timezone.utc)
    else:
        statut   = "en_attente"
        date_pub = None
        # Un doctorant ne peut pas marquer comme peer_reviewed lui-même
        data     = data.model_copy(update={"peer_reviewed": False})

    pub = Publication(
        **data.model_dump(),
        auteur_id=current_user.id,
        statut=statut,
        date_publication=date_pub,
    )
    db.add(pub)
    db.commit()
    db.refresh(pub)
    return pub


@router.get("/{pub_id}", response_model=PublicationOut)
def get_publication(
    pub_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[Utilisateur] = Depends(get_current_user_optional),
):
    pub = db.get(Publication, pub_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publication introuvable")
    if not _can_see(pub, current_user):
        raise HTTPException(status_code=403, detail="Accès refusé")
    return pub


@router.patch("/{pub_id}", response_model=PublicationOut)
def update_publication(
    pub_id: int,
    data: PublicationUpdate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    pub = db.get(Publication, pub_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publication introuvable")
    if pub.auteur_id != current_user.id and current_user.role.libelle not in ("super_admin", "admin_axe"):
        raise HTTPException(status_code=403, detail="Accès refusé")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(pub, field, value)
    db.commit()
    db.refresh(pub)
    return pub


@router.post("/{pub_id}/valider", response_model=PublicationOut)
def valider_publication(
    pub_id: int,
    data: ValidationRequest,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(require_role("super_admin", "admin_axe", "chercheur")),
):
    """Validation par un chercheur, admin_axe ou super_admin.
    Un doctorant ne peut jamais valider une publication."""
    pub = db.get(Publication, pub_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publication introuvable")
    if pub.statut != "en_attente":
        raise HTTPException(status_code=400, detail="Publication non en attente de validation")

    if data.decision == "approuver":
        pub.statut           = "publie"
        pub.date_publication = datetime.now(timezone.utc)
        pub.peer_reviewed    = True  # marqué peer-reviewed après validation humaine
    elif data.decision == "rejeter":
        pub.statut = "rejete"
    else:
        raise HTTPException(status_code=400, detail="Décision invalide : 'approuver' ou 'rejeter'")

    pub.validateur_id    = current_user.id
    pub.date_validation  = datetime.now(timezone.utc)
    db.commit()
    db.refresh(pub)
    return pub


@router.post("/{pub_id}/upload-pdf")
async def upload_pdf(
    pub_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    pub = db.get(Publication, pub_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publication introuvable")
    if pub.auteur_id != current_user.id and current_user.role.libelle != "super_admin":
        raise HTTPException(status_code=403, detail="Accès refusé")
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Seuls les fichiers PDF sont acceptés")

    upload_dir = os.path.join(settings.UPLOAD_DIR, "publications")
    os.makedirs(upload_dir, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.pdf"
    path = os.path.join(upload_dir, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    pub.fichier_pdf_url = path
    db.commit()
    return {"fichier_pdf_url": path}


@router.delete("/{pub_id}", status_code=204)
def delete_publication(
    pub_id: int,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    pub = db.get(Publication, pub_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publication introuvable")
    if pub.auteur_id != current_user.id and current_user.role.libelle != "super_admin":
        raise HTTPException(status_code=403, detail="Accès refusé")
    db.delete(pub)
    db.commit()
