from typing import List

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from models.db_models import Candidate, Process
from services.db_service import db_service

router = APIRouter(tags=["Candidates"])


@router.get("/processes/{process_id}/candidates", response_model=list[Candidate])
async def get_candidates_for_process(process_id: int):
    async with db_service.get_session() as session:
        # ensure process exists
        query = select(Process).where(Process.id == process_id)
        process = (await session.exec(query)).first()
        if not process:
            raise HTTPException(status_code=404, detail="Process not found")

        # candidates via relationship
        return process.candidates


@router.get("/candidates/search/{name}", response_model=List[Candidate])
async def search_candidate_by_name(name: str):
    async with db_service.get_session() as session:
        statement = select(Candidate).where(Candidate.nom.contains(name))
        results = (await session.exec(statement)).all()

        if not results:
            raise HTTPException(status_code=404, detail="No matching candidate found")

        return results


@router.get("/candidates/{candidate_id}", response_model=Candidate)
async def get_candidate_by_id(candidate_id: int):
    async with db_service.get_session() as session:
        query = select(Candidate).where(Candidate.id == candidate_id)
        candidate = (await session.exec(query)).first()

        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")

        return candidate


@router.post("/candidates", response_model=Candidate)
async def create_candidate(candidate: Candidate):
    async with db_service.get_session() as session:
        session.add(candidate)
        await session.commit()
        session.refresh(candidate)
        return candidate
