-- ============================================================
--  Portail UMMISCO — Script MySQL
--  Projet IPDL DIC1 · ESP/UCAD
--  Généré automatiquement — à adapter selon l'environnement
-- ============================================================

CREATE DATABASE IF NOT EXISTS ummisco_portail
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE ummisco_portail;

-- ------------------------------------------------------------
-- 1. GESTION DES ACCÈS (ACL)
-- ------------------------------------------------------------

CREATE TABLE role (
  id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  libelle     VARCHAR(80)  NOT NULL UNIQUE,
  description TEXT,
  created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE permission (
  id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  action      ENUM('create','read','update','delete') NOT NULL,
  entite      VARCHAR(80) NOT NULL,               -- ex: 'publication', 'dataset', 'utilisateur'
  description TEXT,
  UNIQUE KEY uq_perm (action, entite)
) ENGINE=InnoDB;

CREATE TABLE role_permission (
  role_id       INT UNSIGNED NOT NULL,
  permission_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (role_id, permission_id),
  CONSTRAINT fk_rp_role       FOREIGN KEY (role_id)       REFERENCES role(id)       ON DELETE CASCADE,
  CONSTRAINT fk_rp_permission FOREIGN KEY (permission_id) REFERENCES permission(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 2. UTILISATEURS
-- ------------------------------------------------------------

CREATE TABLE utilisateur (
  id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nom           VARCHAR(100) NOT NULL,
  prenom        VARCHAR(100) NOT NULL,
  email         VARCHAR(191) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role_id       INT UNSIGNED NOT NULL,
  statut        ENUM('actif','inactif','suspendu') NOT NULL DEFAULT 'actif',
  langue        ENUM('fr','en') NOT NULL DEFAULT 'fr',
  avatar_url    VARCHAR(500),
  bio           TEXT,
  created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_util_role FOREIGN KEY (role_id) REFERENCES role(id)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 3. AXES THÉMATIQUES
-- ------------------------------------------------------------

CREATE TABLE axe_thematique (
  id             INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nom            VARCHAR(150) NOT NULL,
  description    TEXT,
  responsable_id INT UNSIGNED,               -- chercheur responsable de l'axe
  couleur_hex    VARCHAR(7),                 -- ex: '#1D9E75' pour l'UI
  created_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_axe_responsable FOREIGN KEY (responsable_id) REFERENCES utilisateur(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- Appartenance d'un utilisateur à un ou plusieurs axes
CREATE TABLE utilisateur_axe (
  utilisateur_id INT UNSIGNED NOT NULL,
  axe_id         INT UNSIGNED NOT NULL,
  role_axe       ENUM('membre','responsable','doctorant') NOT NULL DEFAULT 'membre',
  PRIMARY KEY (utilisateur_id, axe_id),
  CONSTRAINT fk_ua_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id) ON DELETE CASCADE,
  CONSTRAINT fk_ua_axe         FOREIGN KEY (axe_id)         REFERENCES axe_thematique(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 4. PUBLICATIONS
-- ------------------------------------------------------------

CREATE TABLE publication (
  id               INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  titre            VARCHAR(500) NOT NULL,
  resume           TEXT,
  auteur_id        INT UNSIGNED NOT NULL,
  axe_id           INT UNSIGNED,
  visibilite       ENUM('public','prive','protege') NOT NULL DEFAULT 'public',
  -- Statut du workflow de validation
  statut           ENUM('brouillon','en_attente','publie','rejete') NOT NULL DEFAULT 'brouillon',
  -- Si peer_reviewed = TRUE → publication directe sans validation interne
  peer_reviewed    TINYINT(1) NOT NULL DEFAULT 0,
  doi              VARCHAR(255),
  url_scholar      VARCHAR(500),
  revue            VARCHAR(300),
  annee            YEAR,
  fichier_pdf_url  VARCHAR(500),
  validateur_id    INT UNSIGNED,             -- admin qui a validé (NULL si direct)
  date_validation  TIMESTAMP,
  date_publication TIMESTAMP,
  created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_pub_auteur     FOREIGN KEY (auteur_id)     REFERENCES utilisateur(id),
  CONSTRAINT fk_pub_axe        FOREIGN KEY (axe_id)        REFERENCES axe_thematique(id) ON DELETE SET NULL,
  CONSTRAINT fk_pub_validateur FOREIGN KEY (validateur_id) REFERENCES utilisateur(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- Auteurs multiples sur une même publication
CREATE TABLE publication_auteur (
  publication_id INT UNSIGNED NOT NULL,
  utilisateur_id INT UNSIGNED NOT NULL,
  ordre          TINYINT UNSIGNED NOT NULL DEFAULT 1,
  PRIMARY KEY (publication_id, utilisateur_id),
  CONSTRAINT fk_pa_pub  FOREIGN KEY (publication_id) REFERENCES publication(id) ON DELETE CASCADE,
  CONSTRAINT fk_pa_util FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 5. DATASETS
-- ------------------------------------------------------------

CREATE TABLE dataset (
  id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  titre           VARCHAR(300) NOT NULL,
  description     TEXT,
  proprietaire_id INT UNSIGNED NOT NULL,
  axe_id          INT UNSIGNED,
  visibilite      ENUM('public','prive','protege') NOT NULL DEFAULT 'protege',
  licence         VARCHAR(100),              -- ex: 'CC BY 4.0', 'MIT', 'Propriétaire'
  fichier_path    VARCHAR(500),
  taille_octets   BIGINT UNSIGNED,
  format          VARCHAR(50),               -- ex: 'CSV', 'JSON', 'NetCDF'
  version         VARCHAR(20) DEFAULT '1.0',
  mots_cles       VARCHAR(500),
  created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_ds_proprietaire FOREIGN KEY (proprietaire_id) REFERENCES utilisateur(id),
  CONSTRAINT fk_ds_axe          FOREIGN KEY (axe_id)          REFERENCES axe_thematique(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 6. PROJETS & PARTENAIRES
-- ------------------------------------------------------------

CREATE TABLE partenaire (
  id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nom         VARCHAR(200) NOT NULL,
  type        ENUM('academique','institutionnel','industriel','ong','autre') NOT NULL,
  pays        VARCHAR(100),
  contact     VARCHAR(191),
  logo_url    VARCHAR(500),
  site_web    VARCHAR(500),
  created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE projet (
  id             INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  titre          VARCHAR(300) NOT NULL,
  description    TEXT,
  responsable_id INT UNSIGNED NOT NULL,
  axe_id         INT UNSIGNED,
  date_debut     DATE,
  date_fin       DATE,
  statut         ENUM('en_cours','termine','suspendu','planifie') NOT NULL DEFAULT 'planifie',
  budget         DECIMAL(15,2),
  created_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_proj_responsable FOREIGN KEY (responsable_id) REFERENCES utilisateur(id),
  CONSTRAINT fk_proj_axe         FOREIGN KEY (axe_id)         REFERENCES axe_thematique(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE projet_partenaire (
  projet_id       INT UNSIGNED NOT NULL,
  partenaire_id   INT UNSIGNED NOT NULL,
  role_partenaire VARCHAR(150),
  PRIMARY KEY (projet_id, partenaire_id),
  CONSTRAINT fk_pp_projet     FOREIGN KEY (projet_id)     REFERENCES projet(id)     ON DELETE CASCADE,
  CONSTRAINT fk_pp_partenaire FOREIGN KEY (partenaire_id) REFERENCES partenaire(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Membres d'un projet (chercheurs, doctorants)
CREATE TABLE projet_membre (
  projet_id      INT UNSIGNED NOT NULL,
  utilisateur_id INT UNSIGNED NOT NULL,
  role_projet    VARCHAR(100),
  PRIMARY KEY (projet_id, utilisateur_id),
  CONSTRAINT fk_pm_projet FOREIGN KEY (projet_id)      REFERENCES projet(id)      ON DELETE CASCADE,
  CONSTRAINT fk_pm_util   FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 7. BAILLEURS & DÉLIVRABLES
-- ------------------------------------------------------------

CREATE TABLE bailleur (
  id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nom        VARCHAR(200) NOT NULL,
  pays       VARCHAR(100),
  contact    VARCHAR(191),
  site_web   VARCHAR(500),
  logo_url   VARCHAR(500),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE delivrable (
  id           INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  projet_id    INT UNSIGNED NOT NULL,
  bailleur_id  INT UNSIGNED,
  titre        VARCHAR(300) NOT NULL,
  description  TEXT,
  fichier_path VARCHAR(500),
  echeance     DATE,
  statut       ENUM('en_cours','soumis','accepte','rejete') NOT NULL DEFAULT 'en_cours',
  created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_del_projet  FOREIGN KEY (projet_id)   REFERENCES projet(id)  ON DELETE CASCADE,
  CONSTRAINT fk_del_bailleur FOREIGN KEY (bailleur_id) REFERENCES bailleur(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 8. ACTUALITÉS & ÉVÉNEMENTS
-- ------------------------------------------------------------

CREATE TABLE actualite (
  id               INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  titre            VARCHAR(300) NOT NULL,
  contenu          LONGTEXT,
  auteur_id        INT UNSIGNED NOT NULL,
  statut           ENUM('brouillon','en_attente','publie','rejete') NOT NULL DEFAULT 'brouillon',
  validateur_id    INT UNSIGNED,
  date_publication TIMESTAMP,
  image_url        VARCHAR(500),
  created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_act_auteur     FOREIGN KEY (auteur_id)     REFERENCES utilisateur(id),
  CONSTRAINT fk_act_validateur FOREIGN KEY (validateur_id) REFERENCES utilisateur(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE evenement (
  id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  titre       VARCHAR(300) NOT NULL,
  description TEXT,
  type        ENUM('conference','seminaire','atelier','these','autre') NOT NULL DEFAULT 'autre',
  date_debut  DATETIME NOT NULL,
  date_fin    DATETIME,
  lieu        VARCHAR(300),
  url_externe VARCHAR(500),
  axe_id      INT UNSIGNED,
  created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_evt_axe FOREIGN KEY (axe_id) REFERENCES axe_thematique(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 9. INTÉGRATIONS EXTERNES (iframes outils doctoraux)
-- ------------------------------------------------------------

CREATE TABLE integration_externe (
  id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nom         VARCHAR(200) NOT NULL,
  description TEXT,
  url_iframe  VARCHAR(500) NOT NULL,
  type        ENUM('simulation','catalogue','capteur','cartographie','autre') NOT NULL,
  axe_id      INT UNSIGNED,
  actif       TINYINT(1) NOT NULL DEFAULT 1,
  created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_ie_axe FOREIGN KEY (axe_id) REFERENCES axe_thematique(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 10. DONNÉES INITIALES (seed)
-- ------------------------------------------------------------

-- Rôles de base
INSERT INTO role (libelle, description) VALUES
  ('super_admin',  'Contrôle total du système'),
  ('admin_axe',    'Administration d'un axe thématique'),
  ('chercheur',    'Publie directement, gère ses données'),
  ('doctorant',    'Publications soumises à validation'),
  ('partenaire',   'Accès lecture + simulations'),
  ('etudiant',     'Accès lecture uniquement'),
  ('visiteur',     'Grand public, accès public uniquement');

-- Permissions CRUD sur les entités principales
INSERT INTO permission (action, entite) VALUES
  ('create','publication'), ('read','publication'), ('update','publication'), ('delete','publication'),
  ('create','dataset'),     ('read','dataset'),     ('update','dataset'),     ('delete','dataset'),
  ('create','actualite'),   ('read','actualite'),   ('update','actualite'),   ('delete','actualite'),
  ('create','projet'),      ('read','projet'),      ('update','projet'),      ('delete','projet'),
  ('create','utilisateur'), ('read','utilisateur'), ('update','utilisateur'), ('delete','utilisateur'),
  ('read','delivrable'),    ('create','delivrable'),
  ('read','integration_externe');

-- Axes thématiques initiaux
INSERT INTO axe_thematique (nom, description) VALUES
  ('Épidémiologie',       'Modélisation et analyse des maladies infectieuses'),
  ('IoT & Science citoyenne', 'Capteurs connectés, données participatives'),
  ('Environnement',       'Climat, sols, biodiversité'),
  ('Cardiologie',         'Systèmes cardiaques, bio-capteurs'),
  ('Géologie',            'Prédiction spatiale, cartographie des sols');

-- Intégrations externes initiales
INSERT INTO integration_externe (nom, description, url_iframe, type, axe_id) VALUES
  ('Catalogue Evelop',     'Catalogue de modèles doctoraux',             'https://evelop.ummisco.ucad.sn', 'catalogue',   NULL),
  ('Prédiction carbone',   'Outil Osman — prédiction spatiale du carbone', 'https://carbone.ummisco.ucad.sn', 'cartographie', 3),
  ('Capteurs arbres',      'Mesure de sève et santé végétale',           'https://capteurs.ummisco.ucad.sn', 'capteur',     2);
