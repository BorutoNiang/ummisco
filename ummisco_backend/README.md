# UMMISCO Backend — API FastAPI

API REST du portail institutionnel UMMISCO · ESP/UCAD · Projet IPDL DIC1

## Stack

- **FastAPI** 0.111 + Uvicorn
- **SQLAlchemy** 2 + PyMySQL (MySQL 8)
- **JWT** (access 60min + refresh 7j)
- **Groq API** — Chat IA Llama 3.3 70B
- **ReportLab** — Génération PDF
- **python-docx / openpyxl** — Remplissage templates Word/Excel

## Démarrage

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m app.services.seed   # BDD + seed initial
uvicorn app.main:app --reload --port 8000
```

API docs : http://localhost:8000/api/docs

## Routes principales

| Méthode | Route | Description |
|---|---|---|
| POST | `/api/v1/auth/login` | Connexion JWT |
| GET | `/api/v1/utilisateurs/` | Liste membres |
| GET/POST | `/api/v1/publications/` | Publications |
| GET/POST | `/api/v1/datasets/` | Datasets |
| GET/POST | `/api/v1/actualites/` | Actualités |
| GET/POST | `/api/v1/projets/` | Projets |
| POST | `/api/v1/chat` | Chat IA Groq |
| POST | `/api/v1/documents/bon-achat/docx` | Bon d'achat |
| POST | `/api/v1/documents/convention-stage/docx` | Convention de stage |
| POST | `/api/v1/documents/prestation-service/xlsx` | Reçu prestation |

## Rôles

| Rôle | Droits |
|---|---|
| `super_admin` (Directeur) | Tout — accès complet |
| `admin_axe` | Administration d'un axe |
| `chercheur` | Publication directe, gestion données |
| `doctorant` | Soumissions à validation |
| `partenaire` | Lecture + simulations |

## Variables d'environnement (.env)

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ummisco_portail
DB_USER=root
DB_PASSWORD=
SECRET_KEY=change_me
GROQ_API_KEY=gsk_...
GROQ_MODEL=llama-3.3-70b-versatile
UPLOAD_DIR=uploads
APP_ENV=development
CORS_ORIGINS=http://localhost:5500
```

## Templates documents

Déposer les fichiers dans `app/templates/` :
- `DEMANDE D'ACHAT.docx`
- `FORMULAIRE+CONVENTION+STAGE (3).docx`
- `Recu de Prestation de Service.xlsx`
