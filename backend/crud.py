from .db import AsyncSessionLocal
from .models import Company, Job
from sqlalchemy import select

async def save_job_if_new(company_id : int , url:str , raw : dict):
    async with AsyncSessionLocal() as session:
        q = await session.execute(select(Job).where(Job.url == url))
        existing = q.scalar_one_or_none()
        if existing:
            return None

        job = Job(company_id= company_id , url = url , raw=raw)
        session.add(job)
        await session.commit()
        await session.refresh(job)
        return job

    async def list_jobs(limit : int = 100):
        async with AsyncSessionLocal() as session:
            q= await session.execute(select(Job).order_by(Job.scraped_at.desc()).limit(limit))
            return q.scalars().all()

    async def get_company(company_id : int):
        async with AsyncSessionLocal() as session:
            return await session.get(Company , company_id)

        