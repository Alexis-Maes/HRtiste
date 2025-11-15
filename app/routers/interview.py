from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["Interviews"])

from services.db_service import db_service
from models.db_models import InterviewCreate, Candidate, Interview, RelevantFields
from sqlmodel import select

from services.claude_service import claude_service
from services import build_prompts
from services import utils 


@router.post("/interviews", response_model=Interview)
async def add_interview(interview_data: InterviewCreate):
    async with db_service.get_session() as session:

        # Validate candidate exists
        candidate = await session.get(Candidate, interview_data.candidate_id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")

        prompt_categories=build_prompts.prompt_decoupe_en_category(interview_data.feedback)
        

        new_fields: RelevantFields = await claude_service.structured_completion(
            inputs=prompt_categories,
            output_model=RelevantFields
        )

        merged_fields = await utils.merge_relevant_fields(candidate, new_fields)

        for field_name, value in merged_fields.__dict__.items():
            setattr(candidate, field_name, value)

        session.add(candidate)

        interview = Interview(
            recruiter_name=interview_data.recruiter_name,
            candidate_id=interview_data.candidate_id,
            feedback=interview_data.feedback_recruiter,
            date=interview_data.date,
        )



        session.add(interview)
        await session.commit()
        await session.refresh(interview)

        return interview


@router.get("/interviews", response_model=list[Interview])
async def get_all_interviews():
    async with db_service.get_session() as session:

        result = await session.exec(
            select(Interview)
        )
        interviews = result.all()
        return interviews
