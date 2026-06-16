"""
documents.py — Remplissage des templates Word/Excel et téléchargement .docx/.xlsx
Routes réservées au super_admin (Directeur)
"""
import io
import copy
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.core.security import require_role

router = APIRouter(prefix="/documents", tags=["Documents"])
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


# ── Helpers python-docx ───────────────────────────────────────────────────────

def _set_para_text(para, text: str):
    """Remplace le texte d'un paragraphe en conservant le style du premier run."""
    if not para.runs:
        para.add_run(text)
        return
    # Vider tous les runs sauf le premier, y mettre le texte
    for i, run in enumerate(para.runs):
        run.text = text if i == 0 else ""


def _fill_para(para, replacements: dict):
    """Remplace les placeholders dans un paragraphe run par run, puis sur le texte assemblé."""
    full = "".join(r.text for r in para.runs)
    for key, val in replacements.items():
        full = full.replace(key, str(val))
    if para.runs:
        para.runs[0].text = full
        for r in para.runs[1:]:
            r.text = ""
    else:
        para.add_run(full)


def _fill_doc(doc, replacements: dict):
    """Applique les remplacements sur tous les paragraphes et cellules."""
    for para in doc.paragraphs:
        _fill_para(para, replacements)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    _fill_para(para, replacements)


def _docx_bytes(doc) -> bytes:
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf.read()


def _docx_response(doc, filename: str) -> StreamingResponse:
    return StreamingResponse(
        io.BytesIO(_docx_bytes(doc)),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


def _xlsx_response(wb, filename: str) -> StreamingResponse:
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


# ── Schémas ───────────────────────────────────────────────────────────────────

class LigneBonAchat(BaseModel):
    objet: str = ""
    fournisseur: str = ""
    prix_unitaire: float = 0
    quantite: int = 1

class BonAchatRequest(BaseModel):
    demandeur: str = ""
    service: str = ""
    eotp: str = ""
    date: str = ""
    adresse: str = ""
    lignes: List[LigneBonAchat] = []

class ConventionStageRequest(BaseModel):
    nom_etablissement: str = ""
    statut_juridique: str = ""
    siege: str = ""
    representant: str = ""
    nom_stagiaire: str = ""
    prenom_stagiaire: str = ""
    adresse_stagiaire: str = ""
    tel_stagiaire: str = ""
    email_stagiaire: str = ""
    annee_universitaire: str = ""
    diplome: str = ""
    specialite: str = ""
    date_debut: str = ""
    date_fin: str = ""
    lieu_stage: str = ""
    structure_accueil: str = ""
    encadrant: str = ""
    montant_mensuel: str = ""
    transport: str = ""
    restauration: str = ""
    imputation: str = ""

class PrestationRequest(BaseModel):
    nom: str = ""
    prenoms: str = ""
    ne_le: str = ""
    a: str = ""
    adresse: str = ""
    tel: str = ""
    emploi_fonction: str = ""
    objet_prestation: str = ""
    produits_attendus: str = ""
    date_debut: str = ""
    date_fin: str = ""
    responsable_suivi: str = ""
    montant_net: float = 0
    montant_net_lettres: str = ""
    service_ur: str = ""
    imputation_eotp: str = ""
    date_acquit: str = ""


# ── BON D'ACHAT ───────────────────────────────────────────────────────────────

@router.post("/bon-achat/docx")
def generer_bon_achat(data: BonAchatRequest, _=Depends(require_role("super_admin"))):
    from docx import Document
    from docx.oxml.ns import qn
    import copy

    tpl = TEMPLATES_DIR / "DEMANDE D'ACHAT.docx"
    if not tpl.exists():
        raise HTTPException(404, "Template introuvable")

    doc = Document(str(tpl))

    # Remplir les paragraphes d'en-tête
    replacements = {
        "NOM ET PRENOM(S) DU DEMANDEUR :": f"NOM ET PRENOM(S) DU DEMANDEUR : {data.demandeur}",
        "SERVICE ou STRUCTURE :": f"SERVICE ou STRUCTURE : {data.service}",
        "EOTP ou CENTRE DE COÛT :": f"EOTP ou CENTRE DE COÛT : {data.eotp}",
        "Dakar le :": f"Dakar le : {data.date}",
    }
    for para in doc.paragraphs:
        for key, val in replacements.items():
            if key in para.text:
                _set_para_text(para, val)

    # Remplir le tableau : ligne de données (index 1) + adresse (dernière ligne)
    if doc.tables:
        tbl = doc.tables[0]
        # Ligne de données = row index 1
        data_row = tbl.rows[1] if len(tbl.rows) > 1 else None

        if data_row and data.lignes:
            # Dupliquer la ligne de données pour chaque article supplémentaire
            from docx.oxml import OxmlElement
            ref_row_xml = data_row._tr

            for i, ligne in enumerate(data.lignes):
                if i == 0:
                    target_row = data_row
                else:
                    # Cloner la ligne de référence
                    new_tr = copy.deepcopy(ref_row_xml)
                    ref_row_xml.addnext(new_tr)
                    # Récupérer la nouvelle ligne
                    target_row = tbl.rows[i + 1]

                cells = target_row.cells
                total = ligne.prix_unitaire * ligne.quantite
                vals = [
                    ligne.objet,
                    ligne.fournisseur,
                    f"{ligne.prix_unitaire:,.0f}" if ligne.prix_unitaire else "",
                    str(ligne.quantite),
                    f"{total:,.0f}" if total else "",
                ]
                for ci, v in enumerate(vals):
                    if ci < len(cells):
                        _set_para_text(cells[ci].paragraphs[0], v)

        # Remplir adresse de livraison (dernière ligne)
        last_row = tbl.rows[-1]
        for para in last_row.cells[0].paragraphs:
            if "Adresse de Livraison" in para.text:
                _set_para_text(para, f"Adresse de Livraison : {data.adresse}")

    return _docx_response(doc, "bon-achat.docx")


# ── CONVENTION DE STAGE ───────────────────────────────────────────────────────

@router.post("/convention-stage/docx")
def generer_convention_stage(data: ConventionStageRequest, _=Depends(require_role("super_admin"))):
    from docx import Document

    tpl = TEMPLATES_DIR / "FORMULAIRE+CONVENTION+STAGE (3).docx"
    if not tpl.exists():
        raise HTTPException(404, "Template introuvable")

    doc = Document(str(tpl))

    # Remplacements dans tout le document
    replacements = {
        # Lignes à compléter après les deux-points
        "NOM :": f"NOM : {data.nom_etablissement}",
        "STATUT JURIDIQUE :": f"STATUT JURIDIQUE : {data.statut_juridique}",
        "SIEGE :": f"SIEGE : {data.siege}",
        "REPRESENTANT LEGAL :": f"REPRESENTANT LEGAL : {data.representant}",
        "Nom et prénom(s) :": f"Nom et prénom(s) : {data.prenom_stagiaire} {data.nom_stagiaire}",
        "Adresse :": f"Adresse : {data.adresse_stagiaire}",
        "Tél :": f"Tél : {data.tel_stagiaire}",
        "Email :": f"Email : {data.email_stagiaire}",
        "Année universitaire :": f"Année universitaire : {data.annee_universitaire}",
        "Diplôme préparé :": f"Diplôme préparé : {data.diplome}",
        "Spécialité :": f"Spécialité : {data.specialite}",
        "du :": f"du : {data.date_debut}",
        "au :": f"au : {data.date_fin}",
        "Lieu :": f"Lieu : {data.lieu_stage}",
        "Structure d'accueil :": f"Structure d'accueil : {data.structure_accueil}",
        "Encadrant(e) :": f"Encadrant(e) : {data.encadrant}",
        "Mensuel :": f"Mensuel : {data.montant_mensuel}",
        "Transport :": f"Transport : {data.transport}",
        "Restauration :": f"Restauration : {data.restauration}",
        "Imputation :": f"Imputation : {data.imputation}",
    }
    _fill_doc(doc, replacements)

    # Table signatures
    if doc.tables:
        sig_tbl = doc.tables[0]
        if len(sig_tbl.rows) > 1:
            row = sig_tbl.rows[1]
            cells = row.cells
            if len(cells) >= 3:
                _set_para_text(cells[0].paragraphs[0], data.representant)
                _set_para_text(cells[1].paragraphs[0], f"{data.prenom_stagiaire} {data.nom_stagiaire}")

    return _docx_response(doc, "convention-stage.docx")


# ── PRESTATION DE SERVICE ─────────────────────────────────────────────────────

@router.post("/prestation-service/xlsx")
def generer_prestation_service(data: PrestationRequest, _=Depends(require_role("super_admin"))):
    import openpyxl

    tpl = TEMPLATES_DIR / "Recu de Prestation de Service.xlsx"
    if not tpl.exists():
        raise HTTPException(404, "Template introuvable")

    wb = openpyxl.load_workbook(str(tpl))
    montant = float(data.montant_net)
    impot = round(montant * 0.05, 2) if montant >= 25000 else 0
    brut = montant + impot

    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        cell_map = {
            "A6": data.nom,
            "D6": data.prenoms,
            "A7": f"né(e) le : {data.ne_le}",
            "D7": f"à : {data.a}",
            "A8": f"Adresse : {data.adresse}",
            "D8": f"Tél : {data.tel}",
            "A9": f"Emploi/Fonction : {data.emploi_fonction}",
            "A10": data.objet_prestation,
            "A13": data.produits_attendus,
            "A15": f"Du : {data.date_debut}",
            "D15": f"au : {data.date_fin}",
            "A16": f"Responsable du suivi : {data.responsable_suivi}",
            "E20": montant,
            "A21": data.montant_net_lettres,
            "A25": data.service_ur,
            "A26": data.imputation_eotp,
            "A35": "POUR ACQUIT",
            "D35": data.date_acquit,
        }
        if impot > 0:
            cell_map["C23"] = impot
            cell_map["C24"] = brut

        for coord, val in cell_map.items():
            if val not in ("", 0):
                ws[coord] = val

    return _xlsx_response(wb, "prestation-service.xlsx")
