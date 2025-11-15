from fastapi import APIRouter, HTTPException
from sqlmodel import select

from services.db_service import db_service
from models.db_models import Interview, Candidate

router = APIRouter(tags=["Interviews"])


@router.get("/interviews")
async def list_interviews():
    """
    Retourne la liste des entretiens avec quelques infos candidat.
    Utile pour afficher / debugger ce qu'il y a en base.
    """
    async with db_service.get_session() as session:
        statement = (
            select(Interview, Candidate)
            .join(Candidate, Candidate.id == Interview.candidate_id)
        )
        result = await session.exec(statement)
        rows = result.all()

        interviews = []
        for interview, candidate in rows:
            interviews.append(
                {
                    "id": interview.id,
                    "date": interview.date,
                    "recruiter_name": interview.recruiter_name,
                    "candidate_id": candidate.id,
                    "candidate_full_name": f"{candidate.prenom} {candidate.nom}",
                    "strengths": interview.strengths,
                    "attention_points": interview.attention_points,
                }
            )

        return interviews


@router.get("/interviews/{interview_id}")
async def get_interview(interview_id: int):
    """
    Retourne le détail d'un entretien spécifique,
    avec les infos du candidat associé.
    """
    async with db_service.get_session() as session:
        statement = (
            select(Interview, Candidate)
            .join(Candidate, Candidate.id == Interview.candidate_id)
            .where(Interview.id == interview_id)
        )
        result = await session.exec(statement)
        row = result.first()

        if not row:
            raise HTTPException(
                status_code=404,
                detail=f"Interview id {interview_id} not found",
            )

        interview, candidate = row

        return {
            "id": interview.id,
            "date": interview.date,
            "recruiter_name": interview.recruiter_name,
            "candidate": {
                "id": candidate.id,
                "prenom": candidate.prenom,
                "nom": candidate.nom,
                "email": candidate.email,
                "numero": candidate.numero,
                "skills": candidate.skills,
                "formations": candidate.formations,
                "experiences": candidate.experiences,
                "description": candidate.description,
            },
            "strengths": interview.strengths,
            "attention_points": interview.attention_points,
            "feedback_recruiter": interview.feedback_recruiter,
            "feedback_candidate": interview.feedback_candidate,
            "recruiter_analysis_perforance": interview.recruiter_analysis_perforance,
        }


@router.get("/candidates/{candidate_id}/interviews")
async def get_interviews_for_candidate(candidate_id: int):
    """
    Liste tous les entretiens d'un candidat donné.
    Pratique si depuis le front tu veux afficher l'historique.
    """
    async with db_service.get_session() as session:
        # Vérifier que le candidat existe
        candidate = await session.get(Candidate, candidate_id)
        if not candidate:
            raise HTTPException(
                status_code=404,
                detail=f"Candidate id {candidate_id} not found",
            )

        statement = select(Interview).where(Interview.candidate_id == candidate_id)
        result = await session.exec(statement)
        interviews = result.all()

        return [
            {
                "id": i.id,
                "date": i.date,
                "recruiter_name": i.recruiter_name,
                "strengths": i.strengths,
                "attention_points": i.attention_points,
                "feedback_recruiter": i.feedback_recruiter,
                "feedback_candidate": i.feedback_candidate,
                "recruiter_analysis_perforance": i.recruiter_analysis_perforance,
            }
            for i in interviews
        ]
