from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import SwapiPerson, Base
from asyncio import run
from os import getenv


DB_NAME = getenv('POSTGRES_DB')
DB_USER = getenv('POSTGRES_USER')
DB_PASSWORD = getenv('POSTGRES_PASSWORD')


DSN = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@postgresql_db:5432/{DB_NAME}'
engine = create_async_engine(DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def paste_to_db(person_json):
    async with Session() as session:
        person_object = SwapiPerson(**person_json)
        session.add(person_object)
        await session.commit()


async def create_tables(engine):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    run(create_tables(engine))
