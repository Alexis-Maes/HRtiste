from typing import List, Optional
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from app.models import Candidate, Recruiter, ProcessCandidateLink, Process, Interview


from .routers import candidate, interview, process, recruiter
from .database import engine

app = FastAPI()



app.include_router(candidate.router) 
app.include_router(interview.router)
app.include_router(process.router)
app.include_router(recruiter.router)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    