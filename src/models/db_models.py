from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Experience(BaseModel):
    company: str
    position: str
    start_date: str
    end_date: str
    job_description: str


class CandidateProfile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: str
