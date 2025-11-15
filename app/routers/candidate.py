from typing import List, Type
from sqlalchemy.orm import selectinload
from fastapi import APIRouter, HTTPException, UploadFile
from sqlmodel import select

from models.db_models import Candidate, Process
from services.db_service import db_service
from services.claude_service import ClaudeService

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
        session.add(candidate)
        await session.commit()
        session.refresh(candidate)
        return candidate




@router.post("/candidates", response_model=Candidate)
async def create_candidate_with_uploaded_cv(cv: UploadFile):

    pdf_bytes = await cv.read()

    try:
        result = ClaudeService.structured_completion(
            inputs="Extrait les informations du candidat depuis ce CV.",
            output_model=Candidate,
            pdf_data=pdf_bytes,
            model="claude-sonnet-4-5"
        )
        import json
        candidate_data = json.loads(result)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors du traitement du CV : {str(e)}")

    db_service.add_element(candidate_data)
