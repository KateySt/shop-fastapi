from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config import db_config

engine = create_async_engine(db_config.DATABASE_URL, echo=True, future=True)

async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
