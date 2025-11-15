from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession


class _DatabaseService:
    def __init__(self):
        super().__init__()
        self.engine: AsyncEngine
        self.async_session: async_sessionmaker[AsyncSession]
        self.initialized = False

    async def initialize(self) -> None:
        self.engine = create_async_engine(
            "postgresql+asyncpg://admin:admin@localhost:5432/profile_manager"
        )
        self.async_session = async_sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def check_initialized(self) -> None:
        if not self.initialized:
            await self.initialize()
            self.initialized = True
        return self

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncGenerator, None]:
        await self.check_initialized()
        async with self.async_session() as session:
            yield session


db_service = _DatabaseService()


async def main():
    await db_service.check_initialized()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
