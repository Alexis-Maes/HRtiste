from fastapi import APIRouter

from models.db_models import Recruiter
from services.db_service import db_service

router = APIRouter(tags=["Recruiters"])


@router.post("/recruiters", response_model=Recruiter)
async def create_recruiter(recruiter: Recruiter):
    async with db_service.get_session() as session:
        await session.add(recruiter)
        await session.commit()
        session.refresh(recruiter)
        return recruiter
