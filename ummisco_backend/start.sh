#!/usr/bin/env bash
# ── Démarrage rapide du backend UMMISCO ──────────────────────
set -e

# 1. Créer l'environnement virtuel si absent
if [ ! -d "venv" ]; then
  echo "→ Création de l'environnement virtuel…"
  python -m venv venv
fi

# 2. Activer
source venv/Scripts/activate 2>/dev/null || source venv/bin/activate

# 3. Installer les dépendances
echo "→ Installation des dépendances…"
pip install -r requirements.txt -q

# 4. Seed initial (idempotent)
echo "→ Seed de la base de données…"
python -m app.services.seed

# 5. Démarrer le serveur
echo "→ Démarrage du serveur FastAPI sur http://localhost:8000"
echo "   Docs : http://localhost:8000/api/docs"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
