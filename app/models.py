from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


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
# Recruiter
# ============================================

class Recruiter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    interviews: List["Interview"] = Relationship(back_populates="recruiter")


# ============================================
# Candidate
# ============================================

class Candidate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    ecole: str
    experience: str
    email: str
    numero: str

    interviews: List["Interview"] = Relationship(back_populates="candidate")

    # Many-to-many with Process
    processes: List["Process"] = Relationship(
        back_populates="candidates",
        link_model=ProcessCandidateLink  # ✔️ class, not string
    )


# ============================================
# Process
# ============================================

class Process(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name_process: str
    job_description: str

    candidates: List[Candidate] = Relationship(
        back_populates="processes",
        link_model=ProcessCandidateLink  # ✔️ class exists already
    )


# ============================================
# Interview
# ============================================

class Interview(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    recruiter_id: int = Field(foreign_key="recruiter.id")
    candidate_id: int = Field(foreign_key="candidate.id")

    feedback: str

    recruiter: Recruiter = Relationship(back_populates="interviews")
    candidate: Candidate = Relationship(back_populates="interviews")



class ProcessCreate(SQLModel):
    name_process: str
    job_description: str
    candidate_ids: Optional[List[int]] = None   # facultatif





class InterviewCreate(SQLModel):
    recruiter_id: int
    candidate_id: int
    feedback: str