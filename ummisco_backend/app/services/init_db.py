"""
init_db.py — Crée les tables puis lance le seed.
Lancer : python -m app.services.init_db
"""
from app.core.database import engine, Base

# Importer tous les modèles pour que SQLAlchemy les enregistre
from app.models import models  # noqa

def init():
    print("→ Création des tables…")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables créées")

    from app.services.seed import seed
    seed()

if __name__ == "__main__":
    init()
