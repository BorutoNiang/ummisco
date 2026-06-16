# Guide d'utilisation — Portail Institutionnel UMMISCO

**Version :** 1.0 · Juin 2026  
**Projet :** IPDL DIC1 · ESP/UCAD · Dakar  
**Équipe :** Projet étudiant — Portail UMI 209 UMMISCO

---

## Table des matières

1. [Présentation du portail](#1-présentation-du-portail)
2. [Accès au portail](#2-accès-au-portail)
3. [Portail public](#3-portail-public)
4. [Connexion à l'intranet](#4-connexion-à-lintranet)
5. [Back-office — Tableau de bord](#5-back-office--tableau-de-bord)
6. [Gestion des publications](#6-gestion-des-publications)
7. [Gestion des datasets](#7-gestion-des-datasets)
8. [Gestion des projets](#8-gestion-des-projets)
9. [Gestion des actualités](#9-gestion-des-actualités)
10. [Gestion des utilisateurs](#10-gestion-des-utilisateurs)
11. [Rôles et permissions](#11-rôles-et-permissions)
12. [Documents administratifs](#12-documents-administratifs)
13. [Chat IA UMMISCO](#13-chat-ia-ummisco)
14. [Maintenance et déploiement](#14-maintenance-et-déploiement)

---

## 1. Présentation du portail

Le portail institutionnel UMMISCO est une application web développée dans le cadre du projet IPDL DIC1 à l'ESP/UCAD. Il offre deux espaces distincts :

- **Portail public** : accessible à tous les visiteurs sans connexion. Il présente les thèmes de recherche, les membres, les projets, les publications et les actualités de l'unité.
- **Intranet (back-office)** : espace sécurisé réservé aux membres authentifiés. Il permet la gestion des contenus, la validation des soumissions et la génération de documents administratifs.

### Technologies utilisées

| Composant | Technologie |
|---|---|
| Frontend | HTML5, CSS3, JavaScript Vanilla |
| Backend | FastAPI (Python 3.11) |
| Base de données | MySQL 8 |
| Authentification | JWT (JSON Web Tokens) |
| IA Chat | Groq API — Llama 3.3 70B |
| Génération documents | python-docx, openpyxl, ReportLab |
| Hébergement | Railway (backend + frontend + BDD) |

---

## 2. Accès au portail

### URLs de production

| Service | URL |
|---|---|
| **Portail public** | https://astonishing-forgiveness-production-12b5.up.railway.app |
| **API Backend** | https://ummisco-production.up.railway.app |
| **Documentation API** | https://ummisco-production.up.railway.app/api/docs |

### Accès local (développement)

```
Frontend : http://localhost:5500
Backend  : http://localhost:8000
API Docs : http://localhost:8000/api/docs
```

---

## 3. Portail public

### Page d'accueil

La page d'accueil présente :
- Un **hero** avec le titre de l'unité, une description et deux boutons d'action (Découvrir l'unité / Actualités)
- Les **4 axes thématiques** sous forme de cartes visuelles
- Les **5 centres régionaux** avec images
- Les **chiffres clés** animés : +1972 publications, 27 partenaires, 29 projets, 94 membres
- Les **tutelles et partenaires** (IRD, Sorbonne, UCAD, Cadi Ayyad, VinUniversity...)
- Un **assistant IA** (bouton chat en bas à droite)

### Navigation principale

La barre de navigation contient :
- **Thèmes** → mega-menu avec les 4 axes (cartes avec images)
- **Centres** → dropdown vers les 5 centres régionaux
- **Projets** → liste des projets réels avec filtres
- **Logiciels** → intégrations et outils doctoraux
- **Membres** → 94 membres avec photos et filtres
- **Publications** → liste des publications avec recherche
- **Actualité** → actualités de l'unité
- **Intranet** → accès à l'espace membres (bouton outline)
- **FR/EN** → sélecteur de langue

### Page Membres

- Affiche les **94 membres réels** de l'UMMISCO avec leur photo officielle, nom, rôle et université
- Données chargées en temps réel depuis l'API officielle d'ummisco.fr
- **Filtres disponibles** : recherche par nom/université, filtre par centre, filtre par rôle
- Clic sur un membre → modal avec photo agrandie, rôle, centre, université

### Page Projets

- **29 projets réels** avec logos (DiDEM, HABITABLE, Waqatali, DigEpi, COMOKIT, etc.)
- Filtre par centre et recherche par nom
- Chaque carte affiche le logo du projet et les centres associés en badges verts

### Page Thèmes (Axes)

Quatre sections détaillées :
1. **Modélisation mathématique et informatique à base d'agents** — EDO, EDP, systèmes multi-agents, COMOKIT
2. **Intelligence Artificielle et Apprentissage Profond** — Deep learning, santé, environnement, AIME, DeepECG4U
3. **Capteurs et collecte de données** — IoT low-cost, FabLabs, Waqatali, AIRQALY
4. **Approches participatives et science citoyenne** — Serious games, crowdsourcing, HABITABLE

### Page Partenaires

- Tutelles et partenaires groupés par centre
- Logos des institutions partenaires
- Filtre par centre

---

## 4. Connexion à l'intranet

### Accès

1. Clique sur le bouton **"Intranet"** dans la navbar (en haut à droite)
2. Tu arrives sur la page de connexion : `/pages/login.html`

### Comptes disponibles

| Rôle | Email | Mot de passe | Description |
|---|---|---|---|
| **Directeur** | admin@ummisco.ucad.sn | Admin@1234 | Accès complet à toutes les fonctionnalités |
| **Chercheur** | chercheur@ummisco.ucad.sn | Demo@1234 | Publication directe, gestion de ses données |
| **Doctorant** | doctorant@ummisco.ucad.sn | Demo@1234 | Soumissions soumises à validation |

### Procédure de connexion

1. Entrer l'adresse e-mail
2. Entrer le mot de passe
3. Cliquer **"Se connecter"**
4. En cas de succès → redirection automatique vers le dashboard

> **Astuce :** Les boutons de démonstration dans la section "Comptes de démonstration" remplissent automatiquement le formulaire. Un simple clic suffit pour vous connecter rapidement.

### Déconnexion

- Clic sur le bouton **"Déconnexion"** en bas de la sidebar gauche

---

## 5. Back-office — Tableau de bord

### Vue d'ensemble

Le tableau de bord est la première page après connexion. Il présente :

**KPIs (indicateurs clés) :**
- Nombre total de publications
- Nombre de datasets
- Éléments en attente de validation (publications + actualités)
- Nombre de membres actifs

**Publications en attente de validation :**
- Liste des publications soumises par les chercheurs/doctorants
- Boutons "Approuver" et "Rejeter" directement depuis le dashboard
- Affichage du nom de l'auteur et de la date de soumission

**Activité récente :**
- Dernières publications et actualités créées

**Publications par axe thématique :**
- Graphique en barres horizontal (animé)
- Permet de voir la répartition des travaux par axe

**Actualités en attente, Datasets à valider, Projets à activer :**
- Trois colonnes de validation rapide
- Actions directement depuis le dashboard

---

## 6. Gestion des publications

### Accès

Sidebar → **Publications**

### Fonctionnalités

**Recherche et filtres :**
- Recherche par titre ou nom d'auteur
- Filtre par statut : Tous / Publié / En attente / Brouillon / Rejeté
- Filtre par axe thématique

**Créer une publication :**
1. Cliquer **"+ Nouvelle publication"**
2. Remplir le formulaire :
   - Titre (obligatoire)
   - Résumé
   - Axe thématique
   - Visibilité (Public / Protégé / Privé)
   - Revue et année de publication
   - DOI (identifiant numérique de l'objet)
   - URL Google Scholar
   - Cocher "Peer-reviewed" si applicable
3. Cliquer **"Enregistrer"**

**Import automatique via DOI :**
1. Coller un DOI dans le champ (ex: `10.1038/s41586-021-03380-y`)
2. Cliquer le bouton **"Importer"** à côté du champ
3. Le système interroge l'API Crossref et remplit automatiquement :
   - Titre complet de l'article
   - Nom de la revue
   - Année de publication
   - URL de l'article
   - Coche "Peer-reviewed" si c'est un article de journal
4. Vérifier les données et cliquer **"Enregistrer"**

**Modifier une publication :**
- Cliquer **"Modifier"** sur la ligne souhaitée
- Modifier les champs et cliquer **"Enregistrer"**

**Supprimer une publication :**
- Cliquer **"Supprimer"** → confirmation requise

**Valider une publication (Directeur/Admin axe) :**
- Cliquer **"Valider"** sur une publication "En attente"
- Choisir **"Approuver"** ou **"Rejeter"**
- Possibilité d'ajouter un commentaire de motif

### Statuts de publication

| Statut | Description | Qui peut publier |
|---|---|---|
| **Brouillon** | Créé mais non soumis | Tous |
| **En attente** | Soumis, en cours de validation | Doctorants |
| **Publié** | Visible publiquement | Chercheurs, Admin, Directeur |
| **Rejeté** | Refusé par un validateur | — |

---

## 7. Gestion des datasets

### Accès

Sidebar → **Datasets**

### Fonctionnalités

- Créer, modifier, supprimer des jeux de données
- Définir la visibilité : **Public** (tous), **Protégé** (membres connectés), **Privé** (soumis à validation)
- Associer à un axe thématique
- Renseigner : format (CSV, JSON, NetCDF…), licence, mots-clés, version

---

## 8. Gestion des projets

### Accès

Sidebar → **Projets**

### Fonctionnalités

- Liste des projets avec statut (En cours / Planifié / Terminé / Suspendu)
- Créer un projet avec titre, description, responsable, axe, dates, budget
- Modifier ou supprimer un projet existant

---

## 9. Gestion des actualités

### Accès

Sidebar → **Actualités**

### Fonctionnalités

- Créer des actualités avec titre, contenu, image
- Workflow de validation identique aux publications
- Les actualités validées s'affichent sur le portail public

---

## 10. Gestion des utilisateurs

### Accès

Sidebar → **Utilisateurs** *(Directeur uniquement)*

### Fonctionnalités

- Voir tous les membres inscrits avec leur rôle et statut
- Modifier le rôle d'un utilisateur
- Activer / suspendre un compte
- Visualiser les axes associés à chaque membre

---

## 11. Rôles et permissions

### Accès

Sidebar → **Rôles & Permissions** *(Directeur uniquement)*

### Rôles disponibles

| Rôle | Description |
|---|---|
| `super_admin` (Directeur) | Contrôle total du système |
| `admin_axe` | Administration d'un axe thématique |
| `chercheur` | Publie directement, gère ses données |
| `doctorant` | Publications soumises à validation |
| `partenaire` | Accès lecture + simulations |
| `etudiant` | Accès lecture uniquement |
| `visiteur` | Grand public, accès public uniquement |

### Tableau des droits

| Action | Directeur | Admin axe | Chercheur | Doctorant |
|---|---|---|---|---|
| Publier directement | ✓ | ✓ | ✓ | — |
| Soumettre à validation | ✓ | ✓ | ✓ | ✓ |
| Valider publications | ✓ | ✓ | ✓ | — |
| Gérer datasets | ✓ | ✓ | ✓ | Limité |
| Gérer projets | ✓ | ✓ | Limité | — |
| Gérer utilisateurs | ✓ | — | — | — |
| Documents administratifs | ✓ | — | — | — |
| Gérer rôles/permissions | ✓ | — | — | — |
| Tableau de bord complet | ✓ | ✓ | ✓ | ✓ |

---

## 12. Documents administratifs

Ces fonctionnalités sont réservées au **Directeur** (`super_admin`).

---

### 12.1 Bon d'achat

**Accès :** Sidebar → **Bon d'achat**

**Objectif :** Générer une demande de bon d'achat au format Word (`.docx`) basée sur le formulaire officiel IRD/UMMISCO.

**Étapes :**

1. **Section "Informations du demandeur" :**
   - Le nom du Directeur connecté est pré-rempli automatiquement
   - Vérifier ou modifier le service/structure (pré-rempli "UMMISCO ESP/UCAD")
   - Saisir l'EOTP ou le centre de coût (ex: PROJ-2025-001)
   - La date du jour est pré-remplie automatiquement
   - Saisir l'adresse de livraison

2. **Section "Articles commandés" :**
   - Cliquer **"+ Ajouter une ligne"** pour chaque article
   - Pour chaque ligne, renseigner :
     - Description de l'article
     - Nom du fournisseur
     - Prix unitaire en FCFA
     - Quantité
     - Le total par ligne se calcule automatiquement
   - Le total général s'affiche en bas
   - Pour supprimer une ligne : cliquer le bouton rouge ✕

3. Cliquer **"Télécharger Word"**
4. Le fichier `bon-achat.docx` se télécharge automatiquement
5. Ouvrir dans Microsoft Word ou LibreOffice → imprimer ou sauvegarder en PDF

---

### 12.2 Convention de stage

**Accès :** Sidebar → **Convention de stage**

**Objectif :** Générer une convention de stage au format Word (`.docx`) basée sur le modèle officiel IRD-Sénégal.

**Étapes :**

1. **Section "Établissement d'enseignement" :**
   - Nom de l'organisme (ex: ESP — École Supérieure Polytechnique)
   - Statut juridique (ex: Établissement public)
   - Siège social (ex: Dakar, Sénégal)
   - Représentant légal (nom et fonction)

2. **Section "Informations du stagiaire" :**
   - Nom et prénom(s) du stagiaire
   - Adresse complète
   - Numéro de téléphone
   - Adresse e-mail
   - Année universitaire (ex: 2025-2026)
   - Diplôme préparé (ex: Master 2 Informatique)
   - Spécialité

3. **Section "Détails du stage" :**
   - Date de début et date de fin
   - Lieu du stage (ex: UMMISCO — ESP/UCAD, Dakar)
   - Structure d'accueil (ex: UMMISCO / IRD)
   - Nom de l'encadrant scientifique

4. **Section "Gratification" :**
   - Montant mensuel en FCFA
   - Indemnité de transport en FCFA
   - Indemnité de restauration en FCFA
   - Code d'imputation / EOTP

5. Cliquer **"Générer"**
6. Le fichier `convention-stage.docx` se télécharge avec tous les articles de la convention pré-remplis

---

### 12.3 Reçu de prestation de service

**Accès :** Sidebar → **Prestation de service**

**Objectif :** Générer un reçu de prestation de service au format Excel (`.xlsx`) basé sur le modèle officiel IRD.

**Étapes :**

1. **Section "Identité du prestataire" :**
   - NOM (en majuscules)
   - Prénom(s)
   - Date de naissance
   - Lieu de naissance
   - Adresse complète
   - Numéro de téléphone
   - Emploi / Fonction

2. **Section "Objet de la prestation" :**
   - Description détaillée de la prestation effectuée
   - Livrables / produits attendus
   - Date de début et date de fin
   - Nom du responsable du suivi

3. **Section "Rémunération" :**
   - Montant net en chiffres (FCFA)
   - **Calcul automatique** : si le montant ≥ 25 000 FCFA, l'impôt de 5% est calculé et affiché automatiquement
   - Montant net en lettres (ex: Cinquante mille francs CFA)
   - Service / UR / US (ex: UMMISCO)
   - Imputation EOTP
   - Date d'acquit (date de signature, pré-remplie avec la date du jour)

4. Cliquer **"Générer"**
5. Le fichier `prestation-service.xlsx` se télécharge avec toutes les données remplies

---

## 13. Chat IA UMMISCO

### Accès

Bouton bleu en bas à droite de la page d'accueil (icône bulle de conversation).

### Fonctionnalités

L'assistant IA UMMISCO est propulsé par **Groq** (modèle Llama 3.3 70B). Il peut répondre à des questions sur :

- Les **thèmes de recherche** de l'UMMISCO
- Les **membres** de chaque centre (94 membres avec rôles et universités)
- Les **projets** en cours (DiDEM, HABITABLE, Waqatali, COMOKIT, etc.)
- Les **centres régionaux** et leurs activités
- La **navigation** sur le portail

### Utilisation

1. Cliquer sur le bouton chat en bas à droite
2. Taper votre question dans le champ de saisie
3. Appuyer sur Entrée ou cliquer le bouton envoi
4. L'assistant répond en quelques secondes
5. L'historique de conversation est conservé pendant la session

**Exemples de questions :**
- *"Qui sont les membres du Centre France ?"*
- *"Quels sont les projets du centre Afrique de l'Ouest ?"*
- *"Qu'est-ce que le projet COMOKIT ?"*
- *"Explique-moi le thème Capteurs et collecte de données"*
- *"Qui est Alassane BAH ?"*

---

## 14. Maintenance et déploiement

### Démarrage local

```bash
# Backend FastAPI
cd ummisco_backend
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac
uvicorn app.main:app --reload --port 8000

# Frontend statique
cd ummisco_frontend
python -m http.server 5500
```

### Initialisation de la base de données (première installation)

```bash
# 1. Créer les tables
python -c "from app.core.database import engine, Base; from app.models import models; Base.metadata.create_all(bind=engine); print('Tables créées')"

# 2. Insérer les données initiales (rôles, admin, axes, intégrations)
python -m app.services.seed
```

### Déploiement sur Railway

**Backend :** https://ummisco-production.up.railway.app  
**Frontend :** https://astonishing-forgiveness-production-12b5.up.railway.app

Variables d'environnement nécessaires (service backend) :

```
DATABASE_URL=mysql://...
SECRET_KEY=...
GROQ_API_KEY=gsk_...
GROQ_MODEL=llama-3.3-70b-versatile
APP_ENV=production
CORS_ORIGINS=https://astonishing-forgiveness-production-12b5.up.railway.app
```

### Mettre à jour le déploiement

Tout commit sur la branche `main` du repo GitHub `BorutoNiang/ummisco` déclenche automatiquement un redéploiement sur Railway.

```bash
git add .
git commit -m "description des modifications"
git push origin main
```

---

*Guide rédigé par l'équipe IPDL DIC1 · ESP/UCAD · Dakar · Juin 2026*
