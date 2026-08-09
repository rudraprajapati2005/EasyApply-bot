# backend/scrapers/generic_scraper.py
# Purpose: generic career page scraper that extracts candidate job links.
# Why: many companies use custom pages; this heuristic finds likely job links.

import re
from urllib.parse import urljoin
from .base_scraper import BaseScraper

KEYWORDS = re.compile(r"(intern|internship|entry|graduate|fresher|trainee|early career)", re.I)

class GenericScraper(BaseScraper):
    async def extract_job_links(self, page_url: str):
        # Open page
        page = await self.open()
        await page.goto(page_url, timeout=60000)

        # Query all anchors and inspect href/text
        anchors = await page.query_selector_all("a")
        links = []
        for a in anchors:
            href = await a.get_attribute("href") or ""
            text = (await a.inner_text()).strip()

            if not href:
                continue

            # Heuristic: link text contains early-career keywords OR href contains job-related words
            if KEYWORDS.search(text) or re.search(r"(job|career|opening|position|opportunity)", href, re.I):
                if href.startswith("/"):
                    href = urljoin(page_url, href)
                links.append(href)

        # Close browser
        await self.close()

        # Deduplicate while preserving order
        seen = set()
        out = []
        for l in links:
            if l not in seen:
                seen.add(l)
                out.append(l)
        return out
