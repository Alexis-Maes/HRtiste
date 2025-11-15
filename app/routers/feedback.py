from fastapi import APIRouter, HTTPException
from sqlmodel import select
from sqlalchemy.orm import selectinload
import json

from models.db_models import (
    Candidate,
    Interview,
    Process,
    RejectionEmailRequest,
    RejectionEmailResponse,
)
from services.db_service import db_service
from services.claude_service import claude_service

router = APIRouter(tags=["Feedback"])


@router.post("/interviews/rejection-email", response_model=RejectionEmailResponse)
async def generate_rejection_email(payload: RejectionEmailRequest) -> RejectionEmailResponse:
    """
    Génère un mail de refus personnalisé à partir :
    - du nom du candidat (full name),
    - des infos déjà présentes en BDD (candidat + dernier entretien + process).
    """

    if payload.decision == "accepted":
        # For now, we only handle rejection emails
        raise HTTPException(
            status_code=400,
            detail="Cette route est pour l'instant dédiée aux mails de refus (decision='rejected').",
        )

    # ============================
    # 1. Retrieve candidate, interview, process from DB
    # ============================
    full_name = payload.candidate_full_name.strip()
    parts = full_name.split()

    if len(parts) < 2:
        raise HTTPException(
            status_code=400,
            detail="Le nom complet du candidat doit contenir au moins un prénom et un nom.",
        )

    first_name = parts[0]
    last_name = " ".join(parts[1:])

    async with db_service.get_session() as session:
        # Load the candidate with related interviews and processes
        stmt = (
            select(Candidate)
            .where(
                Candidate.prenom == first_name,
                Candidate.nom == last_name,
            )
            .options(
                selectinload(Candidate.processes),
                selectinload(Candidate.interviews),
            )
        )

        result = await session.exec(stmt)
        candidate = result.first()

        if not candidate:
            raise HTTPException(
                status_code=404,
                detail=f"Candidat '{full_name}' introuvable en base.",
            )

        # Last candidate interview (the most recent one)
        stmt_interview = (
            select(Interview)
            .where(Interview.candidate_id == candidate.id)
            .order_by(Interview.id.desc())
        )
        result_interview = await session.exec(stmt_interview)
        interview = result_interview.first()

        if not interview:
            raise HTTPException(
                status_code=404,
                detail=f"Aucun entretien trouvé pour le candidat '{full_name}'.",
            )

        # On prend le premier process lié (s'il y en a)
        process = candidate.processes[0] if candidate.processes else None

    # ============================
    # 2. Claude prompt construction
    # ============================
    skills = ", ".join(candidate.skills) if candidate.skills else "N/A"
    formations = ", ".join(candidate.formations) if candidate.formations else "N/A"
    experiences = ", ".join(candidate.experiences) if candidate.experiences else "N/A"

    process_name = payload.process_name or (process.name if process else "votre candidature")
    job_description = process.job_description if process else "N/A"

    recruiter_name = payload.recruiter_name or interview.recruiter_name

    prompt = f"""
Tu es un recruteur RH chargé de rédiger un MAIL DE REFUS bienveillant et personnalisé, en français.

Contexte général :
- Le candidat n'est pas retenu pour le poste, mais on veut lui laisser une très bonne impression.
- Le ton doit être professionnel, chaleureux, respectueux.
- On utilise le vouvoiement.
- On évite tout jugement négatif frontal : on parle plutôt d'adéquation, de priorisation, de critères, etc.

=== POSTE ===
Intitulé du process / poste : {process_name}
Description du poste : {job_description}

=== PROFIL CANDIDAT ===
Prénom : {candidate.prenom}
Nom : {candidate.nom}
Email : {candidate.email}
Numéro : {candidate.numero}

Compétences clé : {skills}
Formations : {formations}
Expériences : {experiences}

Description du profil : {candidate.description}

=== ENTRETIEN RH ===
Date : {interview.date}
Recruteur : {interview.recruiter_name}

Points forts repérés :
{interview.strengths}

Points d'attention :
{interview.attention_points}

Feedback du recruteur :
{interview.feedback_recruiter}

Feedback du candidat :
{interview.feedback_candidate}

Analyse globale de la performance :
{interview.recruiter_analysis_perforance}

=== OBJECTIF ===

Rédige un email de refus que le recruteur {recruiter_name} pourra envoyer au candidat {candidate.prenom} {candidate.nom}.

Contraintes :
- Le mail doit être en français.
- Le ton doit être positif, encourageant, et reconnaissant du temps du candidat.
- Mentionne 2 à 3 points forts concrets issus de l'entretien.
- Explique de manière diplomatique pourquoi la candidature n'est pas retenue (adéquation profil / besoins actuels / autres priorités).
- Propose éventuellement une ouverture (rester en contact, candidatures futures, etc.) si c'est pertinent.
- Termine par une formule de politesse professionnelle.

Format de sortie OBLIGATOIRE : un JSON STRICT avec exactement ces champs :
{{
  "subject": "Objet de l'email",
  "body": "Contenu complet de l'email, avec des sauts de ligne \\n entre les paragraphes."
}}

Ne renvoie STRICTEMENT RIEN d'autre que ce JSON.
Pas de texte avant ou après, pas de markdown, pas de commentaire.
"""

    # ============================
    # 3. Call to Claude API
    # ============================
    completion = await claude_service.completion(
        inputs=prompt,
        max_tokens=800,
        system_prompt="Tu renvoies uniquement du JSON valide correspondant exactement au schéma demandé."
    )

    # Anthropics : we receive the response in chunks, need to concatenate
    text = ""
    for block in completion.content:
        if block.type == "text":
            text += block.text

    # ============================
    # 4. Parsing the JSON response
    # ============================
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="The answer is not a valid JSON",
        )

    if "subject" not in data or "body" not in data:
        raise HTTPException(
            status_code=500,
            detail="The answer don't have the required fields.",
        )

    return RejectionEmailResponse(
        subject=data["subject"],
        body=data["body"],
    )
