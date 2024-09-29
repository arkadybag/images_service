import asyncio

import pytest
import sqlalchemy as sa
from httpx import ASGITransport, AsyncClient
from sqlalchemy import URL, make_url
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.ext.asyncio import create_async_engine

from app.resource.database import create_session_manager
from app.sqlmodel.db import Base
from main import create_app
from settings import Settings


async def database_exists(_url: str) -> bool:
    url: URL = make_url(_url)
    database = url.database
    engine = None

    try:
        text = f"SELECT 1 FROM pg_database WHERE datname='{database}'"
        url = url._replace(database="postgres")
        engine = create_async_engine(url)
        try:
            async with engine.begin() as conn:
                value = await conn.scalar(sa.text(text))
                return bool(value)
        except (ProgrammingError, OperationalError):
            pass
        return False
    finally:
        if engine:
            await engine.dispose()


@pytest.fixture
def app(config):
    yield create_app(config)


async def create_database(_url: str) -> None:
    url: URL = make_url(_url)
    database = url.database
    template = "template1"

    url = url._replace(database="postgres")
    engine = create_async_engine(url, isolation_level="AUTOCOMMIT")
    text = "CREATE DATABASE {} ENCODING '{}' TEMPLATE {}".format(database, "utf8", template)

    async with engine.begin() as conn:
        await conn.execute(sa.text(text))


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def session_factory(config, setup_database):
    yield create_session_manager(config)


@pytest.fixture(scope="session")
def config():
    c = Settings()
    c.POSTGRES_DB = c.TEST_POSTGRES_DB
    yield c


@pytest.fixture(scope="session")
async def engine(config):
    user = config.POSTGRES_USER
    password = config.POSTGRES_PASSWORD
    host = config.POSTGRES_HOST
    port = config.POSTGRES_PORT
    database = config.TEST_POSTGRES_DB

    database_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

    if not await database_exists(database_url):
        await create_database(database_url)

    async_engine = create_async_engine(
        database_url,
        pool_size=10,
        max_overflow=0,
        pool_recycle=1800,
    )

    yield async_engine


@pytest.fixture
async def setup_database(engine):
    Base.metadata.bind = engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
async def client(app):
    async with AsyncClient(base_url="http://test", transport=ASGITransport(app=app)) as cl:
        yield cl


@pytest.fixture()
def test_dataset():
    pass
