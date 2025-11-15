from contextlib import asynccontextmanager

from fastapi import FastAPI

from models.db_models import metadata
from services.db_service import db_service

from .routers import candidate


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup : créer les tables
    await db_service.check_initialized()
    async with db_service.engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)


app.include_router(candidate.router)
# app.include_router(interview.router)
# app.include_router(process.router)
# app.include_router(recruiter.router)
