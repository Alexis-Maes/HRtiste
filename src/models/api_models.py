from typing import List

from pydantic import BaseModel


class SearchParams(BaseModel):
    query: str
    limit: int = 1


class CandidateResponse(BaseModel):
    nom: str
    prenom: str
    email: str
    numero: str

    skills: list[str]
    formations: List[str]
    experiences: List[str]

    business_strengths: str | None = None
    technical_strengths: str | None = None
    fit_strengths: str | None = None

    business_attention_point: str | None = None
    technical_attention_point: str | None = None
    fit_attention_point: str | None = None

    description: str
