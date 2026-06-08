# UMMISCO Frontend — Interface Web

> Interface publique et back-office du portail UMMISCO  
> HTML5 · CSS3 · JavaScript Vanilla (ES6) · Sans framework

---

## Stack technique

| Composant | Description |
|---|---|
| HTML5 | Structure des pages |
| CSS3 | Design system custom (variables, grids, composants) |
| JavaScript ES6 | Logique client, appels API, DOM |
| Fetch API | Communication avec le backend FastAPI |
| localStorage | Persistance tokens JWT + préférences langue |

Aucune dépendance externe — pas de React, Vue, Angular, Bootstrap ou jQuery.

---

## Structure du projet

```
ummisco_frontend/
├── index.html                      # Page d'accueil
├── css/
│   └── global.css                  # Design system complet (~800 lignes)
├── js/
│   ├── api.js                      # Client HTTP, Auth, Toast, helpers
│   ├── nav.js                      # Header + navbar injectés dans toutes les pages
│   ├── admin-layout.js             # Sidebar + topbar back-office
│   └── i18n.js                     # Traduction FR/EN
├── images/
│   ├── logo-ummisco.png            # Logo UMMISCO
│   ├── logo-ucad.png               # Logo UCAD
│   ├── esp.jpg                     # Logo ESP
│   ├── ird.png                     # Logo IRD
│   ├── ugb.jpg                     # Logo UGB
│   ├── hero-accueil.png            # Image hero slider
│   ├── actu-miss-abms.jpg          # Image actualité MISS-ABMS
│   ├── actu-appel-pdi.jpg          # Image actualité PDI
│   ├── actu-ateliers-pecheurs.jpg  # Image actualité ateliers
│   ├── evt-conference.jpg          # Image événement conférence
│   ├── evt-reunion.jpg             # Image événement réunion
│   ├── evt-commisco.jpg            # Image événement Commisco
│   └── evt-seminaire.jpg           # Image événement séminaire
└── pages/
    ├── login.html                  # Page de connexion
    ├── presentation.html           # Présentation de l'unité
    ├── equipe.html                 # Membres et chercheurs
    ├── axes.html                   # Axes thématiques
    ├── publications.html           # Publications scientifiques
    ├── datasets.html               # Données ouvertes
    ├── projets.html                # Projets de recherche
    ├── actualites.html             # Actualités et vie du lab
    ├── partenaires.html            # Partenaires institutionnels
    ├── integrations.html           # Outils et simulations
    ├── contact.html                # Contact et formulaire
    └── admin/
        ├── dashboard.html          # Tableau de bord
        ├── publications.html       # Gestion publications
        ├── datasets.html           # Gestion datasets
        ├── projets.html            # Gestion projets
        ├── actualites.html         # Gestion actualités
        ├── bailleurs.html          # Gestion bailleurs + délivrables
        ├── integrations.html       # Gestion intégrations
        ├── utilisateurs.html       # Gestion utilisateurs
        └── roles.html              # Gestion rôles ACL
```

---

## Démarrage

```bash
cd ummisco_frontend
python -m http.server 5500
```

Ouvrir dans le navigateur : `http://127.0.0.1:5500/index.html`

> Le backend doit tourner sur `http://localhost:8000` pour que les appels API fonctionnent.

---

## Architecture JavaScript

### api.js — Client HTTP

Point d'entrée pour tous les appels au backend.

```javascript
// Appels API
api.get('/publications/?limit=5')
api.post('/auth/login', { email, password })
api.patch('/publications/1', { titre: '...' })
api.delete('/publications/1')
api.upload('/datasets/1/upload', formData)  // multipart

// Gestion de l'authentification
Auth.isLoggedIn()          // Vérifie si connecté
Auth.getToken()            // Access token JWT
Auth.getRole()             // Rôle de l'utilisateur
Auth.can('chercheur', 'super_admin')  // Vérification multi-rôles
Auth.setUser(user)         // Stocke le profil
Auth.clear()               // Déconnexion

// Notifications
Toast.success('Message')
Toast.error('Erreur')
Toast.info('Information')
Toast.warn('Avertissement')

// Helpers
formatDate(isoString)      // "23 juin 2022"
formatDateTime(isoString)  // "Jeudi, 23 juin, 2022 - 09:35"
truncate(str, 100)         // Coupe à 100 caractères
badgeHtml('public')        // Badge HTML coloré
statutBadge('en_attente')  // Badge statut

// Guards
requireAuth(['super_admin'])  // Redirige si pas connecté ou mauvais rôle
redirectIfAuth()              // Redirige vers dashboard si déjà connecté
```

### nav.js — Header partagé

Injecte automatiquement le header institutionnel (topbar + logos + navbar) dans chaque page.

```javascript
// Usage dans chaque page publique
initNav({ active: 'actualites', base: '../' });
initFooter({ base: '../' });

// active : identifiant de la page active dans la navbar
// base   : chemin relatif vers la racine ('' pour index.html, '../' pour pages/)
```

### admin-layout.js — Back-office

Injecte la sidebar et la topbar dans chaque page admin.

```javascript
// Usage dans chaque page admin
initAdminLayout('publications');
// Argument : identifiant de la page active dans la sidebar
```

### i18n.js — Traduction FR/EN

```javascript
// Changer la langue
setLang('en');   // Passe en anglais et recharge
setLang('fr');   // Repasse en français

// Obtenir une traduction
t('nav.home')    // "Accueil" ou "Home" selon la langue courante

// Appliquer toutes les traductions (appelé automatiquement)
applyTranslations();
```

Pour rendre un élément traduisible, ajouter l'attribut `data-i18n` :

```html
<h1 data-i18n="page.pubs.title">Publications</h1>
<button data-i18n="btn.login">Se connecter</button>
```

---

## Design system (global.css)

### Variables CSS

```css
--c-primary:   #003f87;   /* Bleu UCAD */
--c-accent:    #e8001d;   /* Rouge UMMISCO */
--c-bg:        #ffffff;
--c-surface:   #f5f7fa;
--c-text:      #1a1e2d;
--c-text2:     #4a5568;
--c-border:    #dde2ea;
```

### Composants disponibles

| Classe | Description |
|---|---|
| `.btn`, `.btn--primary`, `.btn--ghost`, `.btn--danger` | Boutons |
| `.badge--publie`, `.badge--attente`, `.badge--public` | Badges statut/visibilité |
| `.card` | Carte avec bordure et hover |
| `.modal-overlay`, `.modal` | Fenêtres modales |
| `.form-group`, `.form-input`, `.form-label` | Formulaires |
| `.alert--error`, `.alert--success` | Messages d'alerte |
| `.spinner`, `.skeleton` | Indicateurs de chargement |
| `.grid-2`, `.grid-3`, `.grid-4` | Grilles responsive |
| `.container`, `.container--wide` | Conteneurs centrés |

### Composants spécifiques

| Classe | Description |
|---|---|
| `.topbar-inst` | Barre supérieure institutionnelle bleue |
| `.site-header` | Header avec logos |
| `.main-nav` | Navbar principale avec dropdowns |
| `.hero-slider` | Slider hero avec dots et flèches |
| `.chiffres-section` | Section "UMMISCO en chiffres" |
| `.rubriques-grid` | Grille des rubriques thématiques |
| `.actu-card` | Carte actualité style référence |
| `.evt-home-card` | Carte événement |
| `.partner-logo-item` | Logo partenaire avec hover |
| `.rubrique-card` | Carte rubrique thématique |
| `.site-footer` | Footer multi-colonnes |

---

## Pages publiques — Détail

### index.html
- Slider hero 3 slides (image, overlay, texte, bouton CTA)
- Section actualités pleine largeur avec bouton "voir plus"
- 6 rubriques thématiques (Enjeux, Axes, Projets, Milieux, Épidémiologie, Méthodes) avec modal détail
- Section événements 3 colonnes avec images
- Section "UMMISCO en chiffres" avec compteurs animés
- Partenaires avec vrais logos + hover
- Layout publications + sidebar (axes, événements, liens)

### pages/actualites.html
- Layout liste : image 200x140 à gauche, titre bleu + date + texte à droite
- Recherche en temps réel
- Sidebar événements + liens utiles
- Modal détail avec image pleine largeur

### pages/publications.html
- Filtres par axe (pills) + tri + recherche texte
- Compteur de résultats
- Badges visibilité et peer-reviewed
- Liens DOI, Google Scholar, téléchargement PDF
- Modal détail complet

---

## Back-office — Accès et droits

| Onglet | super_admin | admin_axe | chercheur | doctorant |
|---|---|---|---|---|
| Tableau de bord | ✓ | ✓ | ✓ | ✓ |
| Publications | ✓ | ✓ | ✓ | Proposer |
| Datasets | ✓ | ✓ | ✓ | Proposer |
| Projets | ✓ | ✓ | ✓ | Proposer |
| Actualités | ✓ | ✓ | ✓ | Proposer |
| Bailleurs | ✓ | ✓ | ✓ | — |
| Intégrations | ✓ | ✓ | ✓ | Proposer |
| Utilisateurs | ✓ | — | — | — |
| Rôles & ACL | ✓ | — | — | — |

**Proposer** = peut créer mais la ressource reste en attente de validation par un chercheur ou admin.

---

## Configuration de l'API

L'URL du backend est définie dans `js/api.js` :

```javascript
const API_BASE = 'http://localhost:8000/api/v1';
```

Pour un déploiement en production, modifier cette valeur vers l'URL du serveur.
