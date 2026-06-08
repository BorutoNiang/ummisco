from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import require_role
from app.models.models import Role, Permission, RolePermission
from app.schemas.schemas import RoleCreate, RoleOut, PermissionOut, AssignPermissionsRequest

router = APIRouter(prefix="/admin", tags=["Administration ACL"])


# ── Rôles ─────────────────────────────────────────────────────

@router.get("/roles", response_model=List[RoleOut])
def list_roles(
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin")),
):
    return db.query(Role).all()


@router.post("/roles", response_model=RoleOut, status_code=201)
def create_role(
    data: RoleCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin")),
):
    if db.query(Role).filter(Role.libelle == data.libelle).first():
        raise HTTPException(status_code=409, detail="Rôle déjà existant")
    role = Role(**data.model_dump())
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@router.delete("/roles/{role_id}", status_code=204)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin")),
):
    role = db.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Rôle introuvable")
    db.delete(role)
    db.commit()


# ── Permissions ───────────────────────────────────────────────

@router.get("/permissions", response_model=List[PermissionOut])
def list_permissions(
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin")),
):
    return db.query(Permission).all()


# ── Assignation permissions → rôle ───────────────────────────

@router.put("/roles/{role_id}/permissions", response_model=RoleOut)
def assign_permissions(
    role_id: int,
    data: AssignPermissionsRequest,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin")),
):
    """Remplace entièrement les permissions d'un rôle (idempotent)."""
    role = db.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Rôle introuvable")

    # Supprimer toutes les permissions actuelles
    db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()

    # Réassigner
    for perm_id in data.permission_ids:
        perm = db.get(Permission, perm_id)
        if not perm:
            raise HTTPException(status_code=404, detail=f"Permission {perm_id} introuvable")
        db.add(RolePermission(role_id=role_id, permission_id=perm_id))

    db.commit()
    db.refresh(role)
    return role


@router.get("/roles/{role_id}/permissions", response_model=List[PermissionOut])
def get_role_permissions(
    role_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("super_admin")),
):
    role = db.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Rôle introuvable")
    return [rp.permission for rp in role.permissions]
