from sqlalchemy import (
    Column, Integer, String, Text, Enum, Boolean,
    ForeignKey, DateTime, Date, DECIMAL, BigInteger,
    SmallInteger, func,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


# ── ACL ──────────────────────────────────────────────────────

class Role(Base):
    __tablename__ = "role"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    libelle     = Column(String(80), nullable=False, unique=True)
    description = Column(Text)
    created_at  = Column(DateTime, server_default=func.now())

    utilisateurs = relationship("Utilisateur", back_populates="role")
    permissions  = relationship("RolePermission", back_populates="role", cascade="all, delete")


class Permission(Base):
    __tablename__ = "permission"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    action      = Column(Enum("create", "read", "update", "delete"), nullable=False)
    entite      = Column(String(80), nullable=False)
    description = Column(Text)

    roles = relationship("RolePermission", back_populates="permission", cascade="all, delete")


class RolePermission(Base):
    __tablename__ = "role_permission"
    role_id       = Column(Integer, ForeignKey("role.id", ondelete="CASCADE"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permission.id", ondelete="CASCADE"), primary_key=True)

    role       = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")


# ── Utilisateurs ─────────────────────────────────────────────

class Utilisateur(Base):
    __tablename__ = "utilisateur"
    id            = Column(Integer, primary_key=True, autoincrement=True)
    nom           = Column(String(100), nullable=False)
    prenom        = Column(String(100), nullable=False)
    email         = Column(String(191), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role_id       = Column(Integer, ForeignKey("role.id"), nullable=False)
    statut        = Column(Enum("actif", "inactif", "suspendu"), default="actif")
    langue        = Column(Enum("fr", "en"), default="fr")
    avatar_url    = Column(String(500))
    bio           = Column(Text)
    created_at    = Column(DateTime, server_default=func.now())
    updated_at    = Column(DateTime, server_default=func.now(), onupdate=func.now())

    role           = relationship("Role", back_populates="utilisateurs")
    axes           = relationship("UtilisateurAxe", back_populates="utilisateur", cascade="all, delete")
    publications   = relationship("Publication", foreign_keys="Publication.auteur_id", back_populates="auteur")
    datasets       = relationship("Dataset", back_populates="proprietaire")
    actualites     = relationship("Actualite", foreign_keys="Actualite.auteur_id", back_populates="auteur")
    projets_resp   = relationship("Projet", back_populates="responsable")


class UtilisateurAxe(Base):
    __tablename__ = "utilisateur_axe"
    utilisateur_id = Column(Integer, ForeignKey("utilisateur.id", ondelete="CASCADE"), primary_key=True)
    axe_id         = Column(Integer, ForeignKey("axe_thematique.id", ondelete="CASCADE"), primary_key=True)
    role_axe       = Column(Enum("membre", "responsable", "doctorant"), default="membre")

    utilisateur = relationship("Utilisateur", back_populates="axes")
    axe         = relationship("AxeThematique", back_populates="membres")


# ── Axes thématiques ─────────────────────────────────────────

class AxeThematique(Base):
    __tablename__ = "axe_thematique"
    id             = Column(Integer, primary_key=True, autoincrement=True)
    nom            = Column(String(150), nullable=False)
    description    = Column(Text)
    responsable_id = Column(Integer, ForeignKey("utilisateur.id", ondelete="SET NULL"))
    couleur_hex    = Column(String(7))
    created_at     = Column(DateTime, server_default=func.now())

    membres        = relationship("UtilisateurAxe", back_populates="axe", cascade="all, delete")
    publications   = relationship("Publication", back_populates="axe")
    datasets       = relationship("Dataset", back_populates="axe")
    projets        = relationship("Projet", back_populates="axe")
    evenements     = relationship("Evenement", back_populates="axe")
    integrations   = relationship("IntegrationExterne", back_populates="axe")


# ── Publications ─────────────────────────────────────────────

class Publication(Base):
    __tablename__ = "publication"
    id               = Column(Integer, primary_key=True, autoincrement=True)
    titre            = Column(String(500), nullable=False)
    resume           = Column(Text)
    auteur_id        = Column(Integer, ForeignKey("utilisateur.id"), nullable=False)
    axe_id           = Column(Integer, ForeignKey("axe_thematique.id", ondelete="SET NULL"))
    visibilite       = Column(Enum("public", "prive", "protege"), default="public")
    statut           = Column(Enum("brouillon", "en_attente", "publie", "rejete"), default="brouillon")
    peer_reviewed    = Column(Boolean, default=False)
    doi              = Column(String(255))
    url_scholar      = Column(String(500))
    revue            = Column(String(300))
    annee            = Column(SmallInteger)
    fichier_pdf_url  = Column(String(500))
    validateur_id    = Column(Integer, ForeignKey("utilisateur.id", ondelete="SET NULL"))
    date_validation  = Column(DateTime)
    date_publication = Column(DateTime)
    created_at       = Column(DateTime, server_default=func.now())
    updated_at       = Column(DateTime, server_default=func.now(), onupdate=func.now())

    auteur     = relationship("Utilisateur", foreign_keys=[auteur_id], back_populates="publications")
    validateur = relationship("Utilisateur", foreign_keys=[validateur_id])
    axe        = relationship("AxeThematique", back_populates="publications")
    co_auteurs = relationship("PublicationAuteur", back_populates="publication", cascade="all, delete")


class PublicationAuteur(Base):
    __tablename__ = "publication_auteur"
    publication_id = Column(Integer, ForeignKey("publication.id", ondelete="CASCADE"), primary_key=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateur.id", ondelete="CASCADE"), primary_key=True)
    ordre          = Column(SmallInteger, default=1)

    publication  = relationship("Publication", back_populates="co_auteurs")
    utilisateur  = relationship("Utilisateur")


# ── Datasets ─────────────────────────────────────────────────

class Dataset(Base):
    __tablename__ = "dataset"
    id              = Column(Integer, primary_key=True, autoincrement=True)
    titre           = Column(String(300), nullable=False)
    description     = Column(Text)
    proprietaire_id = Column(Integer, ForeignKey("utilisateur.id"), nullable=False)
    axe_id          = Column(Integer, ForeignKey("axe_thematique.id", ondelete="SET NULL"))
    visibilite      = Column(Enum("public", "prive", "protege"), default="protege")
    licence         = Column(String(100))
    fichier_path    = Column(String(500))
    taille_octets   = Column(BigInteger)
    format          = Column(String(50))
    version         = Column(String(20), default="1.0")
    mots_cles       = Column(String(500))
    created_at      = Column(DateTime, server_default=func.now())
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now())

    proprietaire = relationship("Utilisateur", back_populates="datasets")
    axe          = relationship("AxeThematique", back_populates="datasets")


# ── Partenaires & Projets ─────────────────────────────────────

class Partenaire(Base):
    __tablename__ = "partenaire"
    id         = Column(Integer, primary_key=True, autoincrement=True)
    nom        = Column(String(200), nullable=False)
    type       = Column(Enum("academique", "institutionnel", "industriel", "ong", "autre"), nullable=False)
    pays       = Column(String(100))
    contact    = Column(String(191))
    logo_url   = Column(String(500))
    site_web   = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())

    projets = relationship("ProjetPartenaire", back_populates="partenaire", cascade="all, delete")


class Projet(Base):
    __tablename__ = "projet"
    id             = Column(Integer, primary_key=True, autoincrement=True)
    titre          = Column(String(300), nullable=False)
    description    = Column(Text)
    responsable_id = Column(Integer, ForeignKey("utilisateur.id"), nullable=False)
    axe_id         = Column(Integer, ForeignKey("axe_thematique.id", ondelete="SET NULL"))
    date_debut     = Column(Date)
    date_fin       = Column(Date)
    statut         = Column(Enum("en_cours", "termine", "suspendu", "planifie"), default="planifie")
    budget         = Column(DECIMAL(15, 2))
    created_at     = Column(DateTime, server_default=func.now())

    responsable  = relationship("Utilisateur", back_populates="projets_resp")
    axe          = relationship("AxeThematique", back_populates="projets")
    partenaires  = relationship("ProjetPartenaire", back_populates="projet", cascade="all, delete")
    membres      = relationship("ProjetMembre", back_populates="projet", cascade="all, delete")
    delivrables  = relationship("Delivrable", back_populates="projet", cascade="all, delete")


class ProjetPartenaire(Base):
    __tablename__ = "projet_partenaire"
    projet_id       = Column(Integer, ForeignKey("projet.id", ondelete="CASCADE"), primary_key=True)
    partenaire_id   = Column(Integer, ForeignKey("partenaire.id", ondelete="CASCADE"), primary_key=True)
    role_partenaire = Column(String(150))

    projet     = relationship("Projet", back_populates="partenaires")
    partenaire = relationship("Partenaire", back_populates="projets")


class ProjetMembre(Base):
    __tablename__ = "projet_membre"
    projet_id      = Column(Integer, ForeignKey("projet.id", ondelete="CASCADE"), primary_key=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateur.id", ondelete="CASCADE"), primary_key=True)
    role_projet    = Column(String(100))

    projet      = relationship("Projet", back_populates="membres")
    utilisateur = relationship("Utilisateur")


# ── Bailleurs & Délivrables ───────────────────────────────────

class Bailleur(Base):
    __tablename__ = "bailleur"
    id         = Column(Integer, primary_key=True, autoincrement=True)
    nom        = Column(String(200), nullable=False)
    pays       = Column(String(100))
    contact    = Column(String(191))
    site_web   = Column(String(500))
    logo_url   = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())

    delivrables = relationship("Delivrable", back_populates="bailleur")


class Delivrable(Base):
    __tablename__ = "delivrable"
    id           = Column(Integer, primary_key=True, autoincrement=True)
    projet_id    = Column(Integer, ForeignKey("projet.id", ondelete="CASCADE"), nullable=False)
    bailleur_id  = Column(Integer, ForeignKey("bailleur.id", ondelete="SET NULL"))
    titre        = Column(String(300), nullable=False)
    description  = Column(Text)
    fichier_path = Column(String(500))
    echeance     = Column(Date)
    statut       = Column(Enum("en_cours", "soumis", "accepte", "rejete"), default="en_cours")
    created_at   = Column(DateTime, server_default=func.now())

    projet   = relationship("Projet", back_populates="delivrables")
    bailleur = relationship("Bailleur", back_populates="delivrables")


# ── Actualités & Événements ───────────────────────────────────

class Actualite(Base):
    __tablename__ = "actualite"
    id               = Column(Integer, primary_key=True, autoincrement=True)
    titre            = Column(String(300), nullable=False)
    contenu          = Column(Text)
    auteur_id        = Column(Integer, ForeignKey("utilisateur.id"), nullable=False)
    statut           = Column(Enum("brouillon", "en_attente", "publie", "rejete"), default="brouillon")
    validateur_id    = Column(Integer, ForeignKey("utilisateur.id", ondelete="SET NULL"))
    date_publication = Column(DateTime)
    image_url        = Column(String(500))
    created_at       = Column(DateTime, server_default=func.now())
    updated_at       = Column(DateTime, server_default=func.now(), onupdate=func.now())

    auteur     = relationship("Utilisateur", foreign_keys=[auteur_id], back_populates="actualites")
    validateur = relationship("Utilisateur", foreign_keys=[validateur_id])


class Evenement(Base):
    __tablename__ = "evenement"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    titre       = Column(String(300), nullable=False)
    description = Column(Text)
    type        = Column(Enum("conference", "seminaire", "atelier", "these", "autre"), default="autre")
    date_debut  = Column(DateTime, nullable=False)
    date_fin    = Column(DateTime)
    lieu        = Column(String(300))
    url_externe = Column(String(500))
    axe_id      = Column(Integer, ForeignKey("axe_thematique.id", ondelete="SET NULL"))
    created_at  = Column(DateTime, server_default=func.now())

    axe = relationship("AxeThematique", back_populates="evenements")


# ── Intégrations externes ─────────────────────────────────────

class IntegrationExterne(Base):
    __tablename__ = "integration_externe"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    nom         = Column(String(200), nullable=False)
    description = Column(Text)
    url_iframe  = Column(String(500), nullable=False)
    type        = Column(Enum("simulation", "catalogue", "capteur", "cartographie", "autre"), nullable=False)
    axe_id      = Column(Integer, ForeignKey("axe_thematique.id", ondelete="SET NULL"))
    actif       = Column(Boolean, default=True)
    created_at  = Column(DateTime, server_default=func.now())

    axe = relationship("AxeThematique", back_populates="integrations")
