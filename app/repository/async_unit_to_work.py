from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

class AsyncUnitOfWork:

    def __init__(self):
        self.session_maker = async_sessionmaker(
            bind=create_async_engine("sqlite+aiosqlite:///users_db.db")
        )

    async def __aenter__(self):
        self.session: AsyncSession = self.session_maker()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
            await self.session.close()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()