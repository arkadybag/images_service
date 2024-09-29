from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from settings import Settings


def create_session_manager(_settings: Settings) -> async_sessionmaker[AsyncSession]:
    postgres_url = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
    engine = create_async_engine(
        postgres_url.format(
            user=_settings.POSTGRES_USER,
            password=_settings.POSTGRES_PASSWORD,
            host=_settings.POSTGRES_HOST,
            port=_settings.POSTGRES_PORT,
            database=_settings.POSTGRES_DB,
        ),
        pool_size=5,
        max_overflow=0,
        pool_recycle=60,
    )
    return async_sessionmaker(engine, expire_on_commit=False)
