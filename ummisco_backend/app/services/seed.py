"""
seed.py — Insérer les données initiales dans la base UMMISCO.
Lancer : python -m app.services.seed
"""
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.models import (
    Role, Permission, RolePermission,
    Utilisateur, AxeThematique, IntegrationExterne,
)


def seed():
    db = SessionLocal()
    try:
        # ── Rôles ─────────────────────────────────────────────
        roles_data = [
            ("super_admin",  "Contrôle total du système"),
            ("admin_axe",    "Administration d'un axe thématique"),
            ("chercheur",    "Publie directement, gère ses données"),
            ("doctorant",    "Publications soumises à validation"),
            ("partenaire",   "Accès lecture + simulations"),
            ("etudiant",     "Accès lecture uniquement"),
            ("visiteur",     "Grand public, accès public uniquement"),
        ]
        roles = {}
        for libelle, desc in roles_data:
            r = db.query(Role).filter(Role.libelle == libelle).first()
            if not r:
                r = Role(libelle=libelle, description=desc)
                db.add(r)
                db.flush()
            roles[libelle] = r
        print("✓ Rôles insérés")

        # ── Permissions CRUD ──────────────────────────────────
        entites = ["publication", "dataset", "actualite", "projet",
                   "utilisateur", "delivrable", "integration_externe",
                   "partenaire", "bailleur", "evenement"]
        actions = ["create", "read", "update", "delete"]
        perms = {}
        for entite in entites:
            for action in actions:
                p = db.query(Permission).filter(
                    Permission.action == action, Permission.entite == entite
                ).first()
                if not p:
                    p = Permission(action=action, entite=entite)
                    db.add(p)
                    db.flush()
                perms[(action, entite)] = p
        print("✓ Permissions insérées")

        # ── Assignation permissions par rôle ──────────────────
        def assign(role_libelle, pairs):
            role = roles[role_libelle]
            existing = {(rp.permission.action, rp.permission.entite)
                        for rp in role.permissions}
            for action, entite in pairs:
                if (action, entite) not in existing:
                    db.add(RolePermission(
                        role_id=role.id,
                        permission_id=perms[(action, entite)].id
                    ))

        all_perms = [(a, e) for e in entites for a in actions]

        # super_admin → tout
        assign("super_admin", all_perms)

        # admin_axe → tout sauf supprimer utilisateurs
        assign("admin_axe", [p for p in all_perms if not (p == ("delete", "utilisateur"))])

        # chercheur → CRUD sur ses ressources, lecture sur le reste
        assign("chercheur", [
            ("create", "publication"), ("read", "publication"),
            ("update", "publication"), ("delete", "publication"),
            ("create", "dataset"),     ("read", "dataset"),
            ("update", "dataset"),     ("delete", "dataset"),
            ("create", "actualite"),   ("read", "actualite"),
            ("update", "actualite"),
            ("create", "projet"),      ("read", "projet"),
            ("read", "evenement"),     ("read", "partenaire"),
            ("read", "delivrable"),    ("create", "delivrable"),
        ])

        # doctorant → créer/lire (soumis à validation)
        assign("doctorant", [
            ("create", "publication"), ("read", "publication"),
            ("create", "dataset"),     ("read", "dataset"),
            ("create", "actualite"),   ("read", "actualite"),
            ("read", "evenement"),     ("read", "projet"),
        ])

        # partenaire → lecture + simulations
        assign("partenaire", [
            ("read", "publication"), ("read", "dataset"),
            ("read", "projet"),      ("read", "evenement"),
            ("read", "integration_externe"),
        ])

        # étudiant & visiteur → lecture publique seulement
        for role_name in ("etudiant", "visiteur"):
            assign(role_name, [
                ("read", "publication"), ("read", "actualite"),
                ("read", "evenement"),
            ])

        print("✓ Permissions assignées aux rôles")

        # ── Compte super admin ────────────────────────────────
        admin_email = "admin@ummisco.ucad.sn"
        if not db.query(Utilisateur).filter(Utilisateur.email == admin_email).first():
            admin = Utilisateur(
                nom="Admin",
                prenom="UMMISCO",
                email=admin_email,
                password_hash=hash_password("Admin@1234"),
                role_id=roles["super_admin"].id,
            )
            db.add(admin)
            print(f"✓ Super admin créé : {admin_email} / Admin@1234")
        else:
            print("✓ Super admin déjà existant")

        # ── Axes thématiques ──────────────────────────────────
        axes_data = [
            ("Épidémiologie",          "Modélisation et analyse des maladies infectieuses", "#E53E3E"),
            ("IoT & Science citoyenne","Capteurs connectés, données participatives",        "#38A169"),
            ("Environnement",          "Climat, sols, biodiversité",                        "#2B6CB0"),
            ("Cardiologie",            "Systèmes cardiaques, bio-capteurs",                 "#D69E2E"),
            ("Géologie",               "Prédiction spatiale, cartographie des sols",        "#805AD5"),
        ]
        for nom, desc, couleur in axes_data:
            if not db.query(AxeThematique).filter(AxeThematique.nom == nom).first():
                db.add(AxeThematique(nom=nom, description=desc, couleur_hex=couleur))
        print("✓ Axes thématiques insérés")

        # ── Intégrations externes ─────────────────────────────
        integrations_data = [
            ("Catalogue Evelop",   "Catalogue de modèles doctoraux",
             "https://evelop.ummisco.ucad.sn",   "catalogue"),
            ("Prédiction carbone", "Outil Osman — prédiction spatiale du carbone",
             "https://carbone.ummisco.ucad.sn",  "cartographie"),
            ("Capteurs arbres",    "Mesure de sève et santé végétale",
             "https://capteurs.ummisco.ucad.sn", "capteur"),
        ]
        for nom, desc, url, type_ in integrations_data:
            if not db.query(IntegrationExterne).filter(IntegrationExterne.nom == nom).first():
                db.add(IntegrationExterne(nom=nom, description=desc, url_iframe=url, type=type_))
        print("✓ Intégrations externes insérées")

        db.commit()
        print("\n🎉 Seed terminé avec succès !")

    except Exception as e:
        db.rollback()
        print(f"❌ Erreur : {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
