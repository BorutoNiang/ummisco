"""
chat.py — Route IA via Groq avec données UMMISCO enrichies
"""
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.core.config import settings

router = APIRouter(prefix="/chat", tags=["Chat IA"])

# ── Données membres chargées depuis ummisco.fr ────────────────
_members_context = ""

async def _load_members_context():
    """Charge les membres depuis l'API ummisco.fr une seule fois."""
    global _members_context
    if _members_context:
        return _members_context
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                "https://ummisco.fr/fr/wp-json/eventin-carte/v1/centres",
                headers={"User-Agent": "UMMISCO-Portal/1.0"}
            )
        data = r.json()
        centres = data if isinstance(data, list) else data.get("data", [])

        lines = []
        seen = set()
        for centre in centres:
            nom_centre = centre.get("nom") or centre.get("title", "")
            # Déduplique les centres en doublon (France 1 & 2, etc.)
            if nom_centre in seen:
                continue
            seen.add(nom_centre)
            lines.append(f"\n## {nom_centre}")
            lines.append(f"Adresse: {centre.get('adresse','')}")
            membres = centre.get("membres", [])
            if membres:
                lines.append("Membres:")
                for m in membres:
                    lines.append(f"  - {m['post_title']} ({m['role']}, {m['universite']})")
            projets = centre.get("projets", [])
            if projets:
                lines.append("Projets: " + ", ".join(p["name"] for p in projets))

        _members_context = "\n".join(lines)
    except Exception as e:
        _members_context = "(données membres non disponibles)"
    return _members_context


def _build_system_prompt(members_ctx: str) -> str:
    return f"""Tu es l'assistant virtuel du portail UMMISCO (UMI 209), une unité mixte internationale spécialisée dans la modélisation mathématique et informatique des systèmes complexes pour la science de la durabilité, créée en 2009.

## INFORMATIONS GÉNÉRALES
- 94 membres, 29 projets, 27 partenaires, 1972 publications
- 4 thèmes de recherche, 5 centres régionaux
- Tutelles : IRD, Sorbonne Université, UCAD, Université Cadi Ayyad, VinUniversity

## 4 THÈMES DE RECHERCHE
1. Modélisation mathématique et informatique à base d'agents (EDO, EDP, agents, GAMA)
2. Intelligence Artificielle et Apprentissage Profond (deep learning, santé, environnement)
3. Capteurs et collecte de données (IoT low-cost, FabLabs, pays du Sud)
4. Approches participatives et science citoyenne (serious games, crowdsourcing, COMMOD)

## DONNÉES RÉELLES DES CENTRES ET MEMBRES
{members_ctx}

## INSTRUCTIONS
- Réponds toujours en français par défaut
- Si l'utilisateur pose une question sur un membre, cherche dans les données ci-dessus
- Sois précis sur les noms, rôles et universités des membres
- Pour les projets, cite les vrais noms (COMOKIT, DiDEM, HABITABLE, Waqatali, etc.)
- Si tu ne sais pas, dis-le honnêtement et suggère de visiter ummisco.fr
- Sois concis et utile"""


class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]


@router.post("")
async def chat(req: ChatRequest):
    if not settings.GROQ_API_KEY:
        raise HTTPException(500, "Clé API Groq non configurée")

    members_ctx = await _load_members_context()
    system_prompt = _build_system_prompt(members_ctx)

    messages = [{"role": "system", "content": system_prompt}]
    messages += [{"role": m.role, "content": m.content} for m in req.messages[-10:]]

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.GROQ_MODEL,
                "messages": messages,
                "max_tokens": 600,
                "temperature": 0.6,
            },
        )

    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"Erreur Groq: {resp.text}")

    reply = resp.json()["choices"][0]["message"]["content"]
    return {"reply": reply}
