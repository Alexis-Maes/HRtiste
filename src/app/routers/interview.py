from fastapi import APIRouter, HTTPException
from sqlmodel import select

router = APIRouter(tags=["Interviews"])

from src.services import build_prompts
from src.services import claude_service
from src.services.db_service import db_service
from src.models.db_models import InterviewCreate, Candidate, Interview, RelevantFields

from src.services.utils import (
    merge_relevant_fields,
    candidate_to_schema,
    RelevantFieldsSchema,
)

@router.post("/interviews", response_model=Interview)
async def add_interview(interview_data: InterviewCreate):
    async with db_service.get_session() as session:

        # 1) Validate candidate exists
        candidate = await session.get(Candidate, interview_data.candidate_id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")

        # 2) Convert candidate DB → Pydantic schema
        candidate_schema = candidate_to_schema(candidate)

        # 3) Extract categories from feedback
        prompt_categories = build_prompts.prompt_decoupe_en_category(
            interview_data.feedback_recruiter
        )

        # 4) IA structured extraction → RelevantFieldsSchema
        new_fields_schema: RelevantFieldsSchema = await claude_service.structured_completion(
            inputs=prompt_categories,
            output_model=RelevantFieldsSchema
        )

        # 5) Merge existing candidate fields with new_fields using AI
        merged_fields = await merge_relevant_fields(candidate_schema, new_fields_schema)

        # 6) Apply merged fields back to the SQLModel candidate
        for field_name, value in merged_fields.dict().items():
            setattr(candidate, field_name, value)

        session.add(candidate)

        # 7) Create interview DB entry
        interview = Interview(
            recruiter_name=interview_data.recruiter_name,
            candidate_id=interview_data.candidate_id,
            feedback_recruiter=interview_data.feedback_recruiter,
            date=interview_data.date,
        )

        session.add(interview)
        await session.commit()
        await session.refresh(interview)

        return interview



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
