from . import build_prompts
from .claude_service import claude_service
from ..models.db_models import Candidate, RelevantFields



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



async def merge_relevant_fields(candidate: Candidate, new_fields: RelevantFields) -> RelevantFields:
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

    return RelevantFields(**merged)