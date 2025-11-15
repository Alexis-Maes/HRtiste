from typing import List, Optional
from fastapi import FastAPI, HTTPException, APIRouter
from sqlmodel import SQLModel, Field, Session, create_engine, select
from app.models import Candidate, Recruiter, ProcessCandidateLink, Process, Interview
from ..database import engine

router = APIRouter(tags= ['Candidates'])

@router.get("/processes/{process_id}/candidates", response_model=List[Candidate])
def get_candidates_for_process(process_id: int):
    with Session(engine) as session:

        # ensure process exists
        process = session.get(Process, process_id)
        if not process:
            raise HTTPException(status_code=404, detail="Process not found")

        # candidates via relationship
        return process.candidates
    


@router.get("/candidates/search/{name}", response_model=List[Candidate])
def search_candidate_by_name(name: str):
    with Session(engine) as session:
        statement = select(Candidate).where(
            Candidate.nom.contains(name)
        )
        results = session.exec(statement).all()

        if not results:
            raise HTTPException(status_code=404, detail="No matching candidate found")

        return results
    

@router.get("/candidates/{candidate_id}", response_model=Candidate)
def get_candidate_by_id(candidate_id: int):
    with Session(engine) as session:
        candidate = session.get(Candidate, candidate_id)

        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")

        return candidate
    


@router.post("/candidates", response_model=Candidate)
def create_candidate(candidate: Candidate):
    with Session(engine) as session:
        session.add(candidate)
        session.commit()
        session.refresh(candidate)
        return candidate