from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.security import (
    verify_password, create_access_token, create_refresh_token,
    decode_token, get_current_user
)
from app.models.models import Utilisateur
from app.schemas.schemas import LoginRequest, TokenResponse, RefreshRequest, UtilisateurOut

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Utilisateur).filter(Utilisateur.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    if user.statut != "actif":
        raise HTTPException(status_code=403, detail="Compte suspendu ou inactif")

    payload = {"sub": str(user.id), "role": user.role.libelle}
    return TokenResponse(
        access_token=create_access_token(payload),
        refresh_token=create_refresh_token(payload),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(data: RefreshRequest):
    payload = decode_token(data.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Token de rafraîchissement invalide")
    new_payload = {"sub": payload["sub"], "role": payload.get("role")}
    return TokenResponse(
        access_token=create_access_token(new_payload),
        refresh_token=create_refresh_token(new_payload),
    )


@router.get("/me", response_model=UtilisateurOut)
def get_me(current_user=Depends(get_current_user)):
    return current_user
