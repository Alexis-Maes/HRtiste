from typing import List, Optional
from fastapi import FastAPI, HTTPException, APIRouter
from sqlmodel import SQLModel, Field, Session, create_engine, select
from app.models import Candidate, Recruiter, ProcessCandidateLink, Process, Interview
from ..database import engine


router = APIRouter(tags= ['Recruiters'])

@router.post("/recruiters", response_model=Recruiter)
def create_recruiter(recruiter: Recruiter):
    with Session(engine) as session:
        session.add(recruiter)
        session.commit()
        session.refresh(recruiter)
        return recruiter