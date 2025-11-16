from . import build_prompts
from .claude_service import claude_service
from typing import List, Optional
from pydantic import BaseModel


class CandidateSchema(BaseModel):
    id: Optional[int] = None
    nom: str
    prenom: str
    email: str
    numero: str

    skills: List[str] = []
    formations: List[str] = []
    experiences: List[str] = []

    business_strengths: Optional[str] = None
    technical_strengths: Optional[str] = None
    fit_strengths: Optional[str] = None

    business_attention_point: Optional[str] = None
    technical_attention_point: Optional[str] = None
    fit_attention_point: Optional[str] = None

    description: Optional[str] = None


class RelevantFieldsSchema(BaseModel):
    skills: List[str] = []
    formations: List[str] = []
    experiences: List[str] = []

    business_strengths: Optional[str] = None
    technical_strengths: Optional[str] = None
    fit_strengths: Optional[str] = None

    business_attention_point: Optional[str] = None
    technical_attention_point: Optional[str] = None
    fit_attention_point: Optional[str] = None

    description: Optional[str] = None



async def merge_field_with_ai(
    field_name: str,
    old_value: str | list[str] | None,
    new_value: str | list[str] | None
):
    prompt = build_prompts.prompt_complete_category(
        categorie=field_name,
        ancien_contenu=str(old_value or ""),
        nouveau_contenu=str(new_value or "")
    )

    merged = await claude_service.structured_completion(
        inputs=prompt,
        output_model=str
    )

    return merged



def candidate_to_schema(candidate_db) -> CandidateSchema:
    return CandidateSchema(
        id=candidate_db.id,
        nom=candidate_db.nom,
        prenom=candidate_db.prenom,
        email=candidate_db.email,
        numero=candidate_db.numero,

        skills=candidate_db.skills or [],
        formations=candidate_db.formations or [],
        experiences=candidate_db.experiences or [],

        business_strengths=candidate_db.business_strengths,
        technical_strengths=candidate_db.technical_strengths,
        fit_strengths=candidate_db.fit_strengths,

        business_attention_point=candidate_db.business_attention_point,
        technical_attention_point=candidate_db.technical_attention_point,
        fit_attention_point=candidate_db.fit_attention_point,

        description=candidate_db.description,)



async def merge_relevant_fields(candidate: CandidateSchema, new_fields: RelevantFieldsSchema) -> RelevantFieldsSchema:
    merged = {}

    for field_name, value in new_fields.__dict__.items():
        old_value = getattr(candidate, field_name, "")
        new_value = value

        merged_value = await merge_field_with_ai(
            field_name=field_name,
            old_value=old_value,
            new_value=new_value
        )

        merged[field_name] = merged_value

    return RelevantFieldsSchema(**merged)