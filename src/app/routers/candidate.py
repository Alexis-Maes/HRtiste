from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import select
from profile_manager import update_description
from src.models.api_models import CandidateResponse, SearchParams
from src.models.db_models import Candidate, Process
from src.profile_manager import search_candidates
from src.services.db_service import db_service

router = APIRouter(tags=["Candidates"])


@router.get("/processes/{process_id}/candidates", response_model=list[Candidate])
async def get_candidates_for_process(process_id: int):
    async with db_service.get_session() as session:
        # Load process AND preload candidates in one query (async-safe)
        query = (
            select(Process)
            .where(Process.id == process_id)
            .options(selectinload(Process.candidates))
        )

        result = await session.exec(query)
        process = result.one_or_none()

        if not process:
            raise HTTPException(status_code=404, detail="Process not found")

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
        candidate= await update_description(candidate)
        session.add(candidate)
        await session.commit()
        session.refresh(candidate)
        return candidate


@router.post("/candidate/search", response_model=List[CandidateResponse])
async def search_candidates_route(request: SearchParams):
    candidates = await search_candidates(query=request.query, limit=request.limit)
    candidates_response = [
        CandidateResponse(
            nom=candidate.nom,
            prenom=candidate.prenom,
            email=candidate.email,
            numero=candidate.numero,
            skills=candidate.skills,
            formations=candidate.formations,
            experiences=candidate.experiences,
            business_strengths=candidate.business_strengths,
            business_attention_point=candidate.business_attention_point,
            technical_strengths=candidate.technical_strengths,
            technical_attention_point=candidate.technical_attention_point,
            fit_attention_point=candidate.fit_attention_point,
            fit_strengths=candidate.fit_strengths,
            description=candidate.description
        )
        for candidate in candidates
    ]
    return candidates_response
