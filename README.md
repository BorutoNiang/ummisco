# Portail UMMISCO — Projet IPDL DIC1 · ESP/UCAD

Portail institutionnel de l'UMI 209 UMMISCO (Unité Mixte Internationale de Modélisation et Simulation pour le Changement de la Science).

## Stack technique

| Composant | Technologie |
|---|---|
| Frontend | HTML5 · CSS3 · JavaScript Vanilla |
| Backend | FastAPI (Python 3.11) |
| Base de données | MySQL 8 |
| ORM | SQLAlchemy 2 |
| Auth | JWT (access + refresh tokens) |
| IA Chat | Groq API (Llama 3.3 70B) |
| Génération docs | ReportLab · python-docx · openpyxl |

## Structure du projet

```
projetipdl/
├── ummisco_backend/       # API FastAPI
│   ├── app/
│   │   ├── core/          # config, database, security
│   │   ├── models/        # SQLAlchemy models
│   │   ├── routers/       # auth, publications, datasets, chat, documents…
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # seed, init_db
│   │   └── templates/     # Templates Word/Excel pour génération de documents
│   └── requirements.txt
└── ummisco_frontend/      # Interface web statique
    ├── css/global.css
    ├── images/
    ├── js/                # api.js, nav.js, admin-layout.js, i18n.js
    └── pages/
        ├── admin/         # Dashboard, publications, bon-achat, convention-stage…
        └── *.html         # Pages publiques
```

## Démarrage rapide

### Backend
```bash
cd ummisco_backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python -m app.services.seed    # Seed initial (idempotent)
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd ummisco_frontend
python -m http.server 5500
```

- Frontend → http://localhost:5500
- API docs → http://localhost:8000/api/docs

## Comptes de démonstration

| Email | Mot de passe | Rôle |
|---|---|---|
| admin@ummisco.ucad.sn | Admin@1234 | Directeur (super_admin) |
| chercheur@ummisco.ucad.sn | Demo@1234 | Chercheur |
| doctorant@ummisco.ucad.sn | Demo@1234 | Doctorant |

## Fonctionnalités

### Portail public
- Page d'accueil avec chiffres clés, thèmes, centres, tutelles
- Chat IA (Groq · Llama 3.3) avec contexte UMMISCO complet
- Équipe : 94 membres réels depuis l'API ummisco.fr avec photos
- Projets : 29 projets réels avec logos et filtres
- Partenaires : tutelles et partenaires par centre
- Thèmes : 4 axes avec descriptions et images
- Publications, datasets, actualités, intégrations

### Back-office (Directeur)
- Dashboard avec KPIs et validation des soumissions
- Gestion publications, datasets, projets, actualités, utilisateurs
- Génération de documents officiels :
  - **Bon d'achat** (DEMANDE D'ACHAT.docx)
  - **Convention de stage** (.docx rempli)
  - **Reçu de prestation de service** (.xlsx rempli)
- Import de publications via DOI (API Crossref)
- Rôles & permissions

## Variables d'environnement

```env
DB_HOST=localhost
DB_NAME=ummisco_portail
DB_USER=root
DB_PASSWORD=
SECRET_KEY=your_secret_key
GROQ_API_KEY=gsk_...
GROQ_MODEL=llama-3.3-70b-versatile
```
