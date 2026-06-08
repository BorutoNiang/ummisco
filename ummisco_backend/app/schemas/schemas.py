from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


# ── Enums ─────────────────────────────────────────────────────

class StatutEnum(str, Enum):
    actif = "actif"
    inactif = "inactif"
    suspendu = "suspendu"

class VisibiliteEnum(str, Enum):
    public = "public"
    prive = "prive"
    protege = "protege"

class StatutPublicationEnum(str, Enum):
    brouillon = "brouillon"
    en_attente = "en_attente"
    publie = "publie"
    rejete = "rejete"

class StatutProjetEnum(str, Enum):
    en_cours = "en_cours"
    termine = "termine"
    suspendu = "suspendu"
    planifie = "planifie"

class StatutDelivrableEnum(str, Enum):
    en_cours = "en_cours"
    soumis = "soumis"
    accepte = "accepte"
    rejete = "rejete"

class TypeEvenementEnum(str, Enum):
    conference = "conference"
    seminaire = "seminaire"
    atelier = "atelier"
    these = "these"
    autre = "autre"

class TypeIntegrationEnum(str, Enum):
    simulation = "simulation"
    catalogue = "catalogue"
    capteur = "capteur"
    cartographie = "cartographie"
    autre = "autre"

class RoleAxeEnum(str, Enum):
    membre = "membre"
    responsable = "responsable"
    doctorant = "doctorant"


# ── Auth ──────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str


# ── Rôles & Permissions ───────────────────────────────────────

class PermissionOut(BaseModel):
    id: int
    action: str
    entite: str
    description: Optional[str] = None
    model_config = {"from_attributes": True}

class RoleBase(BaseModel):
    libelle: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleOut(RoleBase):
    id: int
    permissions: List[PermissionOut] = []
    model_config = {"from_attributes": True}

    @field_validator("permissions", mode="before")
    @classmethod
    def extract_permissions(cls, v):
        """La relation role.permissions retourne des RolePermission (table jointure).
        On extrait l'objet Permission sous-jacent."""
        result = []
        for item in v:
            # Si c'est un RolePermission, on extrait .permission
            if hasattr(item, "permission"):
                result.append(item.permission)
            else:
                result.append(item)
        return result

# Version légère pour UtilisateurOut (pas besoin des permissions au login)
class RoleSimpleOut(BaseModel):
    id: int
    libelle: str
    description: Optional[str] = None
    model_config = {"from_attributes": True}

class AssignPermissionsRequest(BaseModel):
    permission_ids: List[int]


# ── Utilisateurs ─────────────────────────────────────────────

class UtilisateurCreate(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    password: str
    role_id: int
    langue: Optional[str] = "fr"
    bio: Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères")
        return v

class UtilisateurUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    langue: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    statut: Optional[StatutEnum] = None
    role_id: Optional[int] = None

class UtilisateurOut(BaseModel):
    id: int
    nom: str
    prenom: str
    email: str
    statut: str
    langue: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    role: RoleSimpleOut
    created_at: datetime
    model_config = {"from_attributes": True}

class UtilisateurPublic(BaseModel):
    id: int
    nom: str
    prenom: str
    avatar_url: Optional[str]
    bio: Optional[str]
    model_config = {"from_attributes": True}


# ── Axes thématiques ──────────────────────────────────────────

class AxeCreate(BaseModel):
    nom: str
    description: Optional[str] = None
    responsable_id: Optional[int] = None
    couleur_hex: Optional[str] = None

class AxeUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None
    responsable_id: Optional[int] = None
    couleur_hex: Optional[str] = None

class AxeOut(BaseModel):
    id: int
    nom: str
    description: Optional[str]
    couleur_hex: Optional[str]
    model_config = {"from_attributes": True}


# ── Publications ──────────────────────────────────────────────

class PublicationCreate(BaseModel):
    titre: str
    resume: Optional[str] = None
    axe_id: Optional[int] = None
    visibilite: VisibiliteEnum = VisibiliteEnum.public
    peer_reviewed: bool = False
    doi: Optional[str] = None
    url_scholar: Optional[str] = None
    revue: Optional[str] = None
    annee: Optional[int] = None

class PublicationUpdate(BaseModel):
    titre: Optional[str] = None
    resume: Optional[str] = None
    axe_id: Optional[int] = None
    visibilite: Optional[VisibiliteEnum] = None
    doi: Optional[str] = None
    url_scholar: Optional[str] = None
    revue: Optional[str] = None
    annee: Optional[int] = None

class PublicationOut(BaseModel):
    id: int
    titre: str
    resume: Optional[str]
    visibilite: str
    statut: str
    peer_reviewed: bool
    doi: Optional[str]
    url_scholar: Optional[str]
    revue: Optional[str]
    annee: Optional[int]
    fichier_pdf_url: Optional[str]
    date_publication: Optional[datetime]
    auteur: UtilisateurPublic
    axe: Optional[AxeOut]
    created_at: datetime
    model_config = {"from_attributes": True}

class ValidationRequest(BaseModel):
    decision: str  # "approuver" ou "rejeter"
    commentaire: Optional[str] = None


# ── Datasets ──────────────────────────────────────────────────

class DatasetCreate(BaseModel):
    titre: str
    description: Optional[str] = None
    axe_id: Optional[int] = None
    visibilite: VisibiliteEnum = VisibiliteEnum.protege
    licence: Optional[str] = None
    format: Optional[str] = None
    version: Optional[str] = "1.0"
    mots_cles: Optional[str] = None

class DatasetUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    visibilite: Optional[VisibiliteEnum] = None
    licence: Optional[str] = None
    version: Optional[str] = None
    mots_cles: Optional[str] = None

class DatasetOut(BaseModel):
    id: int
    titre: str
    description: Optional[str]
    visibilite: str
    licence: Optional[str]
    format: Optional[str]
    version: Optional[str]
    mots_cles: Optional[str]
    taille_octets: Optional[int]
    proprietaire: UtilisateurPublic
    axe: Optional[AxeOut]
    created_at: datetime
    model_config = {"from_attributes": True}


# ── Projets ───────────────────────────────────────────────────

class ProjetCreate(BaseModel):
    titre: str
    description: Optional[str] = None
    axe_id: Optional[int] = None
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    budget: Optional[float] = None

class ProjetUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    statut: Optional[StatutProjetEnum] = None
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    budget: Optional[float] = None

class ProjetOut(BaseModel):
    id: int
    titre: str
    description: Optional[str]
    statut: str
    date_debut: Optional[date]
    date_fin: Optional[date]
    budget: Optional[float]
    responsable: UtilisateurPublic
    axe: Optional[AxeOut]
    created_at: datetime
    model_config = {"from_attributes": True}


# ── Partenaires ───────────────────────────────────────────────

class PartenaireCreate(BaseModel):
    nom: str
    type: str
    pays: Optional[str] = None
    contact: Optional[str] = None
    logo_url: Optional[str] = None
    site_web: Optional[str] = None

class PartenaireOut(BaseModel):
    id: int
    nom: str
    type: str
    pays: Optional[str]
    contact: Optional[str]
    logo_url: Optional[str]
    site_web: Optional[str]
    model_config = {"from_attributes": True}


# ── Bailleurs & Délivrables ───────────────────────────────────

class BailleurCreate(BaseModel):
    nom: str
    pays: Optional[str] = None
    contact: Optional[str] = None
    site_web: Optional[str] = None
    logo_url: Optional[str] = None

class BailleurOut(BaseModel):
    id: int
    nom: str
    pays: Optional[str]
    contact: Optional[str]
    logo_url: Optional[str]
    model_config = {"from_attributes": True}

class DelivrableCreate(BaseModel):
    projet_id: int
    bailleur_id: Optional[int] = None
    titre: str
    description: Optional[str] = None
    echeance: Optional[date] = None

class DelivrableUpdate(BaseModel):
    titre: Optional[str] = None
    statut: Optional[StatutDelivrableEnum] = None
    echeance: Optional[date] = None

class DelivrableOut(BaseModel):
    id: int
    titre: str
    description: Optional[str]
    statut: str
    echeance: Optional[date]
    fichier_path: Optional[str]
    bailleur: Optional[BailleurOut]
    model_config = {"from_attributes": True}


# ── Actualités ────────────────────────────────────────────────

class ActualiteCreate(BaseModel):
    titre: str
    contenu: Optional[str] = None
    image_url: Optional[str] = None

class ActualiteOut(BaseModel):
    id: int
    titre: str
    contenu: Optional[str]
    statut: str
    image_url: Optional[str]
    date_publication: Optional[datetime]
    auteur: UtilisateurPublic
    created_at: datetime
    model_config = {"from_attributes": True}


# ── Événements ────────────────────────────────────────────────

class EvenementCreate(BaseModel):
    titre: str
    description: Optional[str] = None
    type: TypeEvenementEnum = TypeEvenementEnum.autre
    date_debut: datetime
    date_fin: Optional[datetime] = None
    lieu: Optional[str] = None
    url_externe: Optional[str] = None
    axe_id: Optional[int] = None

class EvenementOut(BaseModel):
    id: int
    titre: str
    description: Optional[str]
    type: str
    date_debut: datetime
    date_fin: Optional[datetime]
    lieu: Optional[str]
    url_externe: Optional[str]
    axe: Optional[AxeOut]
    model_config = {"from_attributes": True}


# ── Intégrations externes ─────────────────────────────────────

class IntegrationCreate(BaseModel):
    nom: str
    description: Optional[str] = None
    url_iframe: str
    type: TypeIntegrationEnum
    axe_id: Optional[int] = None

class IntegrationOut(BaseModel):
    id: int
    nom: str
    description: Optional[str]
    url_iframe: str
    type: str
    actif: bool
    axe: Optional[AxeOut]
    model_config = {"from_attributes": True}


# ── Pagination générique ──────────────────────────────────────

class PaginatedResponse(BaseModel):
    total: int
    page: int
    per_page: int
    items: list
