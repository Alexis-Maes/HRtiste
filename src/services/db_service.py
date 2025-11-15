from contextlib import asynccontextmanager
from typing import AsyncGenerator, Self

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession


from services.config_service import ConfigService


class _DatabaseService:
    def __init__(self):
        super().__init__()
        self.engine: AsyncEngine
        self.async_session: async_sessionmaker[AsyncSession]
        self.initialized = False

    async def initialize(self) -> None:
        self.engine = create_async_engine(ConfigService.database_url, echo=True)
        self.async_session = async_sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def check_initialized(self) -> Self:
        if not self.initialized:
            await self.initialize()
            self.initialized = True
        return self

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        await self.check_initialized()
        async with self.async_session() as session:
            yield session


db_service = _DatabaseService()
