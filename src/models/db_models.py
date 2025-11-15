from typing import Any, List, Optional, Literal

from pgvector.sqlalchemy import Vector
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Column, Field, Relationship, SQLModel

metadata = SQLModel.metadata
# ============================================
# Association Table (declared FIRST)
# ============================================


class ProcessCandidateLink(SQLModel, table=True):
    process_id: Optional[int] = Field(
        default=None, foreign_key="process.id", primary_key=True
    )
    candidate_id: Optional[int] = Field(
        default=None, foreign_key="candidate.id", primary_key=True
    )


# ============================================
# Candidate
# ============================================


class Candidate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    email: str
    numero: str

    skills: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    formations: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    experiences: List[str] = Field(default_factory=list, sa_column=Column(JSON))

    business_strengths: str = Field(default=None)
    technical_strengths: str = Field(default=None)
    fit_strengths: str = Field(default=None)

    business_attention_point: str = Field(default=None)
    technical_attention_point: str = Field(default=None)
    fit_attention_point: str = Field(default=None)

    description: str
    embeddings: Any = Field(default=None, sa_column=Column(Vector(1024)))

    interviews: List["Interview"] = Relationship(back_populates="candidate")

    # Many-to-many with Process
    processes: List["Process"] = Relationship(
        back_populates="candidates",
        link_model=ProcessCandidateLink,  # ✔️ class, not string
    )


# ============================================
# Process
# ============================================


class Process(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    job_description: str
    required_skills: List[str] = Field(default_factory=list, sa_column=Column(JSON))

    candidates: List[Candidate] = Relationship(
        back_populates="processes",
        link_model=ProcessCandidateLink,  # ✔️ class exists already
    )


# ============================================
# Interview
# ============================================


class Interview(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: str
    recruiter_name: str
    strengths: str
    attention_points: str
    candidate_id: int = Field(foreign_key="candidate.id")

    feedback_recruiter: str
    feedback_candidate: str

    recruiter_analysis_perforance: str
    candidate: Candidate = Relationship(back_populates="interviews")


class PDFModel(BaseModel):
    first_name: str
    last_name: str
    skills: List[str]


class ProcessCreate(SQLModel):
    name_process: str
    job_description: str
    candidate_ids: Optional[List[int]] = None  # facultatif


class InterviewCreate(SQLModel):
    recruiter_id: int
    candidate_id: int
    feedback: str


# ============================================
# Feedback model
# ============================================

class RejectionEmailRequest(BaseModel):
    """
    Payload sent by the front:
    """
    candidate_full_name: str
    decision: Literal["accepted", "rejected"]
    recruiter_name: Optional[str] = None
    process_name: Optional[str] = None


class RejectionEmailResponse(BaseModel):
    """
    Sendback to the front: mail template ready to display / copy.
    """
    subject: str
    body: str
