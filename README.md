# Portail UMMISCO — Documentation générale

> Portail institutionnel de l'Unité Mixte Internationale de Modélisation Mathématique et Informatique des Systèmes Complexes (UMMISCO) · ESP/UCAD · Dakar, Sénégal  
> Projet IPDL DIC1 · École Supérieure Polytechnique

---

## Vue d'ensemble

Le portail UMMISCO est une application web full-stack permettant de gérer et publier les travaux scientifiques de l'unité : publications, datasets, projets, actualités, événements et outils de simulation.

### Architecture

```
projetipdl/
├── ummisco_backend/     # API REST — Python / FastAPI / MySQL
├── ummisco_frontend/    # Interface web — HTML / CSS / JavaScript Vanilla
├── README.md            # Ce fichier
```

### Stack technique

| Composant | Technologie |
|---|---|
| Backend | Python 3.13, FastAPI 0.111, SQLAlchemy 2.0 |
| Base de données | MySQL 8.0 (utf8mb4) |
| Authentification | JWT (access + refresh tokens), bcrypt |
| Frontend | HTML5, CSS3, JavaScript ES6 (Vanilla) |
| Serveur dev frontend | Python http.server |
| Serveur dev backend | Uvicorn avec --reload |

---

## Prérequis

- Python 3.10+
- MySQL 8.0+
- Navigateur moderne (Chrome, Firefox, Edge)

---

## Installation rapide

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd projetipdl
```

### 2. Lancer le backend

```bash
cd ummisco_backend

# Créer l'environnement virtuel
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
cp .env.example .env
# Éditer .env : renseigner DB_PASSWORD, SECRET_KEY

# Créer la base de données MySQL
mysql -u root -p -e "CREATE DATABASE ummisco_portail CHARACTER SET utf8mb4;"

# Initialiser les tables et données de démo
python -m app.services.init_db

# Lancer le serveur
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Lancer le frontend

```bash
cd ummisco_frontend
python -m http.server 5500
```

### 4. Accéder à l'application

| URL | Description |
|---|---|
| http://127.0.0.1:5500/index.html | Page d'accueil publique |
| http://127.0.0.1:5500/pages/login.html | Connexion |
| http://127.0.0.1:5500/pages/admin/dashboard.html | Back-office |
| http://localhost:8000/api/docs | Documentation API (Swagger) |

---

## Comptes de test

| Email | Mot de passe | Rôle |
|---|---|---|
| admin@ummisco.ucad.sn | Admin@1234 | Super administrateur |
| chercheur@ummisco.ucad.sn | Demo@1234 | Chercheur |
| doctorant@ummisco.ucad.sn | Demo@1234 | Doctorant |

---

## Fonctionnalités principales

### Portail public
- Page d'accueil avec slider, actualités, événements, rubriques thématiques, chiffres UMMISCO, partenaires
- 5 axes thématiques de recherche avec statistiques et outils associés
- Publications filtrables par axe, auteur, revue avec visualisation PDF
- Datasets avec contrôle d'accès par visibilité (public / protégé / privé)
- Projets de recherche avec progression temporelle
- Actualités avec images, sidebar événements
- Pages équipe, partenaires, contact, présentation
- **Traduction FR/EN** via boutons dans la topbar

### Back-office (espace membres)
- Dashboard avec KPIs, soumissions en attente, activité récente
- CRUD complet sur toutes les ressources
- Workflow de validation pour les soumissions doctorants
- Gestion des rôles et permissions ACL
- Upload fichiers (PDF, datasets, délivrables)
- Intégrations outils via iframes (Evelop, Osman, Capteurs)

### Workflow de validation (doctorant → chercheur)

| Ressource | Soumis par doctorant | État initial | Action chercheur |
|---|---|---|---|
| Publication | ✓ | en_attente | Approuver / Rejeter |
| Actualité | ✓ | en_attente | Approuver / Rejeter |
| Dataset | ✓ | privé | Changer visibilité |
| Projet | ✓ | suspendu | Activer |
| Intégration | ✓ | inactif | Activer (toggle) |

---

## Rôles et droits

| Action | super_admin | admin_axe | chercheur | doctorant |
|---|---|---|---|---|
| Publication directe | ✓ | ✓ | ✓ | — |
| Soumission (avec validation) | ✓ | ✓ | ✓ | ✓ |
| Valider soumissions | ✓ | ✓ | ✓ | — |
| Gérer intégrations | ✓ | ✓ | ✓ | Proposer |
| Gérer utilisateurs/rôles | ✓ | — | — | — |
| Gérer bailleurs | ✓ | ✓ | ✓ | — |

---

## Auteurs

Projet IPDL DIC1 · École Supérieure Polytechnique (ESP) · UCAD · Dakar, Sénégal
