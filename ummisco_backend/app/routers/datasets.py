from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os, shutil, uuid

from app.core.database import get_db
from app.core.security import get_current_user, get_current_user_optional, require_role
from app.core.config import settings
from app.models.models import Dataset, Utilisateur
from app.schemas.schemas import DatasetCreate, DatasetUpdate, DatasetOut

router = APIRouter(prefix="/datasets", tags=["Datasets"])


def _can_access_dataset(ds: Dataset, user: Optional[Utilisateur]) -> bool:
    if ds.visibilite == "public":
        return True
    if not user:
        return False
    if ds.visibilite == "prive":
        return ds.proprietaire_id == user.id
    # protege → membres UMMISCO (tout rôle sauf visiteur)
    return user.role.libelle != "visiteur"


@router.get("/", response_model=List[DatasetOut])
def list_datasets(
    skip: int = 0,
    limit: int = 20,
    axe_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: Optional[Utilisateur] = Depends(get_current_user_optional),
):
    q = db.query(Dataset)
    if axe_id:
        q = q.filter(Dataset.axe_id == axe_id)
    datasets = q.offset(skip).limit(limit).all()
    return [d for d in datasets if _can_access_dataset(d, current_user)]


@router.post("/", response_model=DatasetOut, status_code=201)
def create_dataset(
    data: DatasetCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    role = current_user.role.libelle
    # Doctorant → dataset privé par défaut (visible uniquement par lui)
    # Un chercheur/admin devra le rendre public ou protégé
    if role in ("doctorant", "etudiant"):
        data = data.model_copy(update={"visibilite": "prive"})
    ds = Dataset(**data.model_dump(), proprietaire_id=current_user.id)
    db.add(ds)
    db.commit()
    db.refresh(ds)
    return ds


@router.get("/{ds_id}", response_model=DatasetOut)
def get_dataset(
    ds_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[Utilisateur] = Depends(get_current_user_optional),
):
    ds = db.get(Dataset, ds_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset introuvable")
    if not _can_access_dataset(ds, current_user):
        raise HTTPException(status_code=403, detail="Accès refusé à ce dataset")
    return ds


@router.patch("/{ds_id}", response_model=DatasetOut)
def update_dataset(
    ds_id: int,
    data: DatasetUpdate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    ds = db.get(Dataset, ds_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset introuvable")
    if ds.proprietaire_id != current_user.id and current_user.role.libelle != "super_admin":
        raise HTTPException(status_code=403, detail="Accès refusé")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(ds, field, value)
    db.commit()
    db.refresh(ds)
    return ds


@router.post("/{ds_id}/upload")
async def upload_fichier(
    ds_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    ds = db.get(Dataset, ds_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset introuvable")
    if ds.proprietaire_id != current_user.id and current_user.role.libelle != "super_admin":
        raise HTTPException(status_code=403, detail="Accès refusé")

    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    contents = await file.read()
    if len(contents) > max_bytes:
        raise HTTPException(status_code=413, detail=f"Fichier trop volumineux (max {settings.MAX_FILE_SIZE_MB} Mo)")

    upload_dir = os.path.join(settings.UPLOAD_DIR, "datasets")
    os.makedirs(upload_dir, exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(upload_dir, filename)
    with open(path, "wb") as f:
        f.write(contents)

    ds.fichier_path = path
    ds.taille_octets = len(contents)
    ds.format = ext.lstrip(".").upper()
    db.commit()
    return {"fichier_path": path, "taille_octets": len(contents)}


@router.delete("/{ds_id}", status_code=204)
def delete_dataset(
    ds_id: int,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    ds = db.get(Dataset, ds_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset introuvable")
    if ds.proprietaire_id != current_user.id and current_user.role.libelle != "super_admin":
        raise HTTPException(status_code=403, detail="Accès refusé")
    db.delete(ds)
    db.commit()
