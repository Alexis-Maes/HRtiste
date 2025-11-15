from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["Interviews"])

from services.db_service import db_service
from models.db_models import Interview, Recruiter, Candidate
from sqlmodel import select


@router.post("/interviews", response_model=Interview)
async def add_interview(interview_data: Interview):
    async with db_service.get_session() as session:

        # Validate recruiter exists
        recruiter = await session.get(Recruiter, interview_data.recruiter_id)
        if not recruiter:
            raise HTTPException(status_code=404, detail="Recruiter not found")

        # Validate candidate exists
        candidate = await session.get(Candidate, interview_data.candidate_id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")

        # Create interview
        interview = Interview(
            recruiter_id=interview_data.recruiter_id,
            candidate_id=interview_data.candidate_id,
            feedback=interview_data.feedback
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
