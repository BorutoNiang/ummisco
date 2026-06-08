# UMMISCO Backend — API REST

> Backend du portail institutionnel UMMISCO  
> Python 3.13 · FastAPI 0.111 · SQLAlchemy 2.0 · MySQL 8

---

## Stack technique

| Composant | Version |
|---|---|
| Python | 3.10+ |
| FastAPI | 0.111.0 |
| SQLAlchemy | 2.0.50 |
| PyMySQL | 1.1.1 |
| python-jose | 3.3.0 |
| passlib + bcrypt | 1.7.4 + 4.0.1 |
| Alembic | 1.13.1 |
| Uvicorn | 0.30.1 |

---

## Structure du projet

```
ummisco_backend/
├── app/
│   ├── main.py                        # Point d'entrée FastAPI, CORS, montage routes
│   ├── core/
│   │   ├── config.py                  # Variables d'environnement (Pydantic Settings)
│   │   ├── database.py                # Engine SQLAlchemy, SessionLocal, Base
│   │   └── security.py               # JWT, bcrypt, dépendances get_current_user, require_role
│   ├── models/
│   │   └── models.py                  # 19 modèles SQLAlchemy (toutes les tables)
│   ├── schemas/
│   │   └── schemas.py                 # 30+ schémas Pydantic (validation I/O)
│   ├── routers/
│   │   ├── auth.py                    # POST /login, /refresh, GET /me
│   │   ├── utilisateurs.py            # CRUD utilisateurs
│   │   ├── axes.py                    # Axes thématiques + membres
│   │   ├── publications.py            # Publications + validation + upload PDF
│   │   ├── datasets.py                # Datasets + upload fichier
│   │   ├── projets.py                 # Projets + partenaires + membres
│   │   ├── partenaires.py             # Partenaires
│   │   ├── bailleurs.py               # Bailleurs + délivrables
│   │   ├── actualites.py              # Actualités + validation
│   │   ├── evenements_integrations.py # Événements + intégrations iframe
│   │   └── admin.py                   # Gestion ACL (rôles + permissions)
│   └── services/
│       ├── seed.py                    # Données initiales (rôles, axes, intégrations, admin)
│       └── init_db.py                 # Création tables + seed (à exécuter une fois)
├── alembic/                           # Migrations (généré par alembic init)
├── alembic.ini
├── requirements.txt
├── .env.example
├── start.bat                          # Démarrage Windows
└── start.sh                          # Démarrage Linux/Mac
```

---

## Installation

### 1. Environnement virtuel

```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac
pip install -r requirements.txt
```

### 2. Configuration

```bash
cp .env.example .env
```

Éditer `.env` :

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ummisco_portail
DB_USER=root
DB_PASSWORD=votre_mdp

SECRET_KEY=une_chaine_aleatoire_longue_et_securisee
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

UPLOAD_DIR=uploads
MAX_FILE_SIZE_MB=50

APP_ENV=development
CORS_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
```

### 3. Base de données

```sql
-- Dans MySQL
CREATE DATABASE ummisco_portail CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Initialisation (tables + données)

```bash
python -m app.services.init_db
```

Crée toutes les tables et insère :
- 7 rôles avec permissions
- 1 compte super admin
- 5 axes thématiques
- 3 intégrations externes

### 5. Démarrage

```bash
# Développement (avec auto-reload)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Ou via le script fourni
start.bat        # Windows
./start.sh       # Linux/Mac
```

---

## API — Endpoints principaux

**Base URL** : `http://localhost:8000/api/v1`  
**Documentation interactive** : `http://localhost:8000/api/docs`

### Authentification

| Méthode | Endpoint | Description |
|---|---|---|
| POST | `/auth/login` | Connexion → tokens JWT |
| POST | `/auth/refresh` | Renouveler le token |
| GET | `/auth/me` | Profil de l'utilisateur connecté |

### Publications

| Méthode | Endpoint | Rôles requis |
|---|---|---|
| GET | `/publications/` | Public |
| POST | `/publications/` | Authentifié |
| PATCH | `/publications/{id}` | Auteur ou admin |
| DELETE | `/publications/{id}` | Auteur ou admin |
| POST | `/publications/{id}/valider` | chercheur, admin_axe, super_admin |
| POST | `/publications/{id}/upload-pdf` | Auteur ou admin |

### Datasets

| Méthode | Endpoint | Rôles requis |
|---|---|---|
| GET | `/datasets/` | Public (filtré par visibilité) |
| POST | `/datasets/` | Authentifié |
| PATCH | `/datasets/{id}` | Propriétaire ou admin |
| POST | `/datasets/{id}/upload` | Propriétaire ou admin |

### Autres ressources

Tous les routers suivent le même pattern REST :
- `GET /ressources/` — liste (filtrée par ACL si besoin)
- `POST /ressources/` — création
- `GET /ressources/{id}` — détail
- `PATCH /ressources/{id}` — modification
- `DELETE /ressources/{id}` — suppression

---

## Modèles de données

### ACL
- `role` — Rôles système (super_admin, admin_axe, chercheur, doctorant, partenaire, etudiant, visiteur)
- `permission` — Actions CRUD sur entités
- `role_permission` — Table de jointure

### Utilisateurs
- `utilisateur` — Compte membre (email unique, bcrypt, statut actif/inactif/suspendu)
- `utilisateur_axe` — Appartenance multi-axes avec rôle dans l'axe

### Contenu scientifique
- `axe_thematique` — 5 axes de recherche
- `publication` — Articles + workflow validation + PDF
- `publication_auteur` — Co-auteurs avec ordre
- `dataset` — Données avec visibilité ACL + fichier
- `projet` — Projets avec budget, dates, statut
- `projet_partenaire` / `projet_membre` — Relations many-to-many

### Gestion
- `bailleur` — Financeurs
- `delivrable` — Livrables de projets avec suivi statut
- `partenaire` — Institutions partenaires
- `actualite` — Flux d'actualités avec workflow validation
- `evenement` — Conférences, séminaires, ateliers
- `integration_externe` — Outils iframes (Evelop, Osman, Capteurs)

---

## Sécurité

### Authentification JWT
```
Authorization: Bearer <access_token>
```

- Access token : 60 minutes
- Refresh token : 7 jours
- Stockage côté client (localStorage)

### Dépendances FastAPI

```python
# Utilisateur obligatoire
current_user = Depends(get_current_user)

# Utilisateur optionnel (routes publiques)
current_user = Depends(get_current_user_optional)

# Restriction par rôle
_ = Depends(require_role("super_admin", "admin_axe"))
```

### Workflow de validation

Les publications et actualités soumises par des doctorants passent en `statut=en_attente`. Un chercheur ou admin valide via `POST /publications/{id}/valider` avec `{"decision": "approuver"}` ou `{"decision": "rejeter"}`.

---

## Variables d'environnement

| Variable | Description | Défaut |
|---|---|---|
| `DB_HOST` | Hôte MySQL | localhost |
| `DB_PORT` | Port MySQL | 3306 |
| `DB_NAME` | Nom de la base | ummisco_portail |
| `DB_USER` | Utilisateur MySQL | root |
| `DB_PASSWORD` | Mot de passe MySQL | (vide) |
| `SECRET_KEY` | Clé JWT (à changer en prod) | changeme |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Durée access token | 60 |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Durée refresh token | 7 |
| `UPLOAD_DIR` | Dossier uploads | uploads |
| `MAX_FILE_SIZE_MB` | Taille max fichier | 50 |
| `APP_ENV` | Environnement | development |
| `CORS_ORIGINS` | Origins CORS autorisées | http://localhost:5500 |
