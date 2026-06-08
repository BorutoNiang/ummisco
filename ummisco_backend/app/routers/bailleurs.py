from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os, shutil, uuid

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.core.config import settings
from app.models.models import Bailleur, Delivrable
from app.schemas.schemas import (
    BailleurCreate, BailleurOut,
    DelivrableCreate, DelivrableUpdate, DelivrableOut,
)

# ── Bailleurs ─────────────────────────────────────────────────

bailleurs_router = APIRouter(prefix="/bailleurs", tags=["Bailleurs"])


@bailleurs_router.get("/", response_model=List[BailleurOut])
def list_bailleurs(db: Session = Depends(get_db)):
    return db.query(Bailleur).all()


@bailleurs_router.post("/", response_model=BailleurOut, status_code=201)
def create_bailleur(
    data: BailleurCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin")),
):
    b = Bailleur(**data.model_dump())
    db.add(b)
    db.commit()
    db.refresh(b)
    return b


@bailleurs_router.get("/{b_id}", response_model=BailleurOut)
def get_bailleur(b_id: int, db: Session = Depends(get_db)):
    b = db.get(Bailleur, b_id)
    if not b:
        raise HTTPException(status_code=404, detail="Bailleur introuvable")
    return b


@bailleurs_router.patch("/{b_id}", response_model=BailleurOut)
def update_bailleur(
    b_id: int,
    data: BailleurCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin")),
):
    b = db.get(Bailleur, b_id)
    if not b:
        raise HTTPException(status_code=404, detail="Bailleur introuvable")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(b, field, value)
    db.commit()
    db.refresh(b)
    return b


@bailleurs_router.delete("/{b_id}", status_code=204)
def delete_bailleur(
    b_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin")),
):
    b = db.get(Bailleur, b_id)
    if not b:
        raise HTTPException(status_code=404, detail="Bailleur introuvable")
    db.delete(b)
    db.commit()


# ── Délivrables ───────────────────────────────────────────────

delivrables_router = APIRouter(prefix="/delivrables", tags=["Délivrables"])


@delivrables_router.get("/", response_model=List[DelivrableOut])
def list_delivrables(
    projet_id: int = None,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe", "chercheur")),
):
    q = db.query(Delivrable)
    if projet_id:
        q = q.filter(Delivrable.projet_id == projet_id)
    return q.all()


@delivrables_router.post("/", response_model=DelivrableOut, status_code=201)
def create_delivrable(
    data: DelivrableCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe", "chercheur")),
):
    d = Delivrable(**data.model_dump())
    db.add(d)
    db.commit()
    db.refresh(d)
    return d


@delivrables_router.patch("/{d_id}", response_model=DelivrableOut)
def update_delivrable(
    d_id: int,
    data: DelivrableUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe")),
):
    d = db.get(Delivrable, d_id)
    if not d:
        raise HTTPException(status_code=404, detail="Délivrable introuvable")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(d, field, value)
    db.commit()
    db.refresh(d)
    return d


@delivrables_router.post("/{d_id}/upload")
async def upload_delivrable(
    d_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin", "admin_axe", "chercheur")),
):
    d = db.get(Delivrable, d_id)
    if not d:
        raise HTTPException(status_code=404, detail="Délivrable introuvable")
    upload_dir = os.path.join(settings.UPLOAD_DIR, "delivrables")
    os.makedirs(upload_dir, exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(upload_dir, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    d.fichier_path = path
    db.commit()
    return {"fichier_path": path}


@delivrables_router.delete("/{d_id}", status_code=204)
def delete_delivrable(
    d_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin")),
):
    d = db.get(Delivrable, d_id)
    if not d:
        raise HTTPException(status_code=404, detail="Délivrable introuvable")
    db.delete(d)
    db.commit()
