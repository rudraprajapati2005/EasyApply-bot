# backend/app.py
# Purpose: FastAPI app exposing endpoints to trigger scrapes and view jobs.
# Why: provides a simple interface for scheduling scrapes and reviewing results.

import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from .scrapers.generic_scraper import GenericScraper
from .crud import save_job_if_new, list_jobs, get_company
from .db import AsyncSessionLocal

app = FastAPI(title="JobBot MVP API")
scraper = GenericScraper()

@app.post("/scrape/")
async def scrape_company(company_id: int, background_tasks: BackgroundTasks):
    """
    Trigger a background scrape for the company with id=company_id.
    We run the heavy work in a background task so the HTTP request returns quickly.
    """
    company = await get_company(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    async def do_scrape(u, cid):
        # Extract links and save new jobs
        links = await scraper.extract_job_links(u)
        for l in links:
            # raw payload stores source and can be extended later
            await save_job_if_new(cid, l, {"source": u})

    background_tasks.add_task(do_scrape, company.career_url, company_id)
    return {"status": "scheduled", "company_id": company_id}

@app.get("/jobs/")
async def get_jobs(limit: int = 100):
    """
    Return recent jobs for review.
    """
    jobs = await list_jobs(limit)
    return {
        "count": len(jobs),
        "jobs": [
            {"id": j.id, "url": j.url, "company_id": j.company_id, "title": j.title, "match_score": j.match_score}
            for j in jobs
        ]
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
