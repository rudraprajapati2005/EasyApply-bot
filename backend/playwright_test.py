# playwright_test.py
# Purpose: verify Playwright and browser binaries are installed and working.
# Why: quick sanity check before running scrapers.

import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.example.com", timeout=60000)
        print("Title:", await page.title())
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
