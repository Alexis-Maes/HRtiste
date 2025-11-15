from typing import List, Optional
from fastapi import FastAPI, HTTPException, APIRouter
from sqlmodel import SQLModel, Field, Session, select
from models.db_models import Candidate, Recruiter, ProcessCandidateLink, Process, Interview
from services.db_service import db_service
from sqlmodel.ext.asyncio.session import AsyncSession


router = APIRouter(tags= ['Recruiters'])

@router.post("/recruiters", response_model=Recruiter)
async def create_recruiter(recruiter: Recruiter):
    async with db_service.get_session() as session:

        session.add(recruiter)
        await session.commit()
        await session.refresh(recruiter)
        return recruiter
    


@router.get("/recruiters", response_model=list[Recruiter])
async def get_recruiters():
    async with db_service.get_session() as session:
        statement = select(Recruiter)
        result = await session.exec(statement)
        recruiters = result.all()
        return recruiters