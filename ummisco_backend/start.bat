@echo off
REM ── Démarrage rapide du backend UMMISCO (Windows) ───────────

REM 1. Créer l'environnement virtuel si absent
if not exist venv (
  echo Création de l'environnement virtuel...
  python -m venv venv
)

REM 2. Activer
call venv\Scripts\activate

REM 3. Installer les dépendances
echo Installation des dépendances...
pip install -r requirements.txt -q

REM 4. Seed initial (idempotent)
echo Seed de la base de données...
python -m app.services.seed

REM 5. Démarrer le serveur
echo.
echo Démarrage du serveur FastAPI sur http://localhost:8000
echo Docs : http://localhost:8000/api/docs
echo.
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
