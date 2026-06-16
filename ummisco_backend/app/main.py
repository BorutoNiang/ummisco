from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.core.database import engine, Base

# Import tous les modèles pour que SQLAlchemy les enregistre
from app.models import models  # noqa

# Import des routers
from app.routers.auth import router as auth_router
from app.routers.utilisateurs import router as users_router
from app.routers.axes import router as axes_router
from app.routers.publications import router as publications_router
from app.routers.datasets import router as datasets_router
from app.routers.projets import router as projets_router
from app.routers.partenaires import router as partenaires_router
from app.routers.bailleurs import bailleurs_router, delivrables_router
from app.routers.actualites import router as actualites_router
from app.routers.evenements_integrations import evenements_router, integrations_router
from app.routers.admin import router as admin_router
from app.routers.documents import router as documents_router
from app.routers.chat import router as chat_router

# ── Création des tables (dev) ─────────────────────────────────
# En production, utiliser Alembic : alembic upgrade head
if settings.APP_ENV == "development":
    Base.metadata.create_all(bind=engine)

# ── App ───────────────────────────────────────────────────────
app = FastAPI(
    title="UMMISCO Portail — API",
    description="Backend du portail institutionnel UMMISCO · Projet IPDL DIC1 · ESP/UCAD",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Fichiers statiques (uploads) ──────────────────────────────
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# ── Routes ────────────────────────────────────────────────────
PREFIX = "/api/v1"

app.include_router(auth_router,          prefix=PREFIX)
app.include_router(users_router,         prefix=PREFIX)
app.include_router(axes_router,          prefix=PREFIX)
app.include_router(publications_router,  prefix=PREFIX)
app.include_router(datasets_router,      prefix=PREFIX)
app.include_router(projets_router,       prefix=PREFIX)
app.include_router(partenaires_router,   prefix=PREFIX)
app.include_router(bailleurs_router,     prefix=PREFIX)
app.include_router(delivrables_router,   prefix=PREFIX)
app.include_router(actualites_router,    prefix=PREFIX)
app.include_router(evenements_router,    prefix=PREFIX)
app.include_router(integrations_router,  prefix=PREFIX)
app.include_router(admin_router,         prefix=PREFIX)
app.include_router(documents_router,     prefix=PREFIX)
app.include_router(chat_router,          prefix=PREFIX)


@app.get("/", tags=["Santé"])
def health_check():
    return {"status": "ok", "app": "UMMISCO Portail API", "version": "1.0.0"}
