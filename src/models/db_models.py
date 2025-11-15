from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Relationship
from typing import List
metadata = SQLModel.metadata

#links many-to-many
class CandidateProcessLink(SQLModel, table=True):
    candidate_id: int = Field(foreign_key="candidateprofile.id", primary_key=True)
    process_id: int = Field(foreign_key="process.id", primary_key=True)


class RecruiterProcessLink(SQLModel, table=True):
    recruiter_id: int = Field(foreign_key="recruiterprofile.id", primary_key=True)
    process_id: int = Field(foreign_key="process.id", primary_key=True)


class Experience(BaseModel):
    company: str
    position: str
    start_date: str
    end_date: str
    job_description: str



class CandidateProfile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    phone: str



class RecruiterProfile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str


class Process(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    number_candidates: int



    # many-to-one depuis Interview
    interviews: List["Interview"] = Relationship(back_populates="process")


class Interview(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    candidate_id: int = Field(foreign_key="candidateprofile.id")
    recruiter_id: int = Field(foreign_key="recruiterprofile.id")
    process_id: int = Field(foreign_key="process.id")

    candidate: CandidateProfile = Relationship(back_populates="interviews")
    recruiter: RecruiterProfile = Relationship(back_populates="interviews")
    process: Process = Relationship(back_populates="interviews")

    date: str
    feedback_recruiter: str | None = None
    feedback_candidate: str | None = None



class PDFModel(BaseModel):
    first_name: str
    last_name: str
    skills: List[str]



