import asyncio
import os

from backend.db import AsyncSessionLocal ,engine ,Base
from backend.models import Company

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def seed():
    await create_tables()
    async with AsyncSessionLocal() as session:
        companies = []

    for c in companies:
        existing = await session.execute(
            __import__("sqlalchemy").select(Company).where(Company.name == c["name"])
        )

        if existing.scalar_one_or_none():
            continue
        company = Company(name=c["name"] , career_url = c["career_url"], ats_type=c["ats_type"])

        session.add(company)

    await session.commit()

if __name__ == "__main__":
    asyncio.run(seed())
    print("Seed complete.")