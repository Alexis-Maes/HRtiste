from sqlmodel import select

from models.db_models import Candidate
from prompts.build_description import BUILD_DESCRIPTION_PROMPT
from services.claude_service import claude_service
from services.db_service import db_service
from services.embedding_service import embedding_service
from utils.claude_utils import extract_text


async def build_candidate_embedding(candidate: Candidate) -> list[float]:
    candidate_embedding = candidate.model_dump(
        include={
            "skills",
            "formations",
            "experiences",
            "business_strengths",
            "technical_strengths",
            "fit_strengths",
            "business_weaknesses",
            "technical_weaknesses",
            "fit_weaknesses",
        }
    )
    inputs = "\n".join(f"{key} - {value}" for key, value in candidate_embedding.items())
    embedding = await embedding_service.get_embedding(text=inputs)
    return embedding


async def build_candidate_description(candidate: Candidate):
    candidate_profile = candidate.model_dump(
        include={
            "skills",
            "formations",
            "experiences",
            "business_strengths",
            "technical_strengths",
            "fit_strengths",
            "business_weaknesses",
            "technical_weaknesses",
            "fit_weaknesses",
        }
    )

    prompt = BUILD_DESCRIPTION_PROMPT.format(description=candidate_profile)
    response = await claude_service.completion(inputs=prompt)
    description = extract_text(response.content)
    return description


async def update_description(candidate: Candidate) -> Candidate:
    candidate.embeddings = await build_candidate_embedding(candidate=candidate)
    candidate.description = await build_candidate_description(candidate=candidate)
    return candidate


async def search_candidates(query: str, limit: int = 1) -> list[Candidate]:
    embedded_query = await embedding_service.get_embedding(text=query)

    async with db_service.get_session() as session:
        query = (
            select(Candidate)
            .order_by(Candidate.embeddings.cosine_distance(embedded_query))
            .limit(limit)
        )
        candidates = (await session.exec(query)).all()
        return candidates
