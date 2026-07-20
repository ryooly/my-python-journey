from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/pokemon_machine"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
