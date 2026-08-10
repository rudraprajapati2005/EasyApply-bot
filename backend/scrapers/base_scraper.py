from playwright.async_api import async_playwright

class BaseScraper:
    async def open(self , headless = True):
        self._pw = await async_playwright().start()
        self._browser = await self._pw.chromium.lauch(headless=headless)
        self._page = await self._browser.new_page()
        return self._page

    async def close(self):
        try:
            await self._browser.close()
        finally:
            await self._pw.stop()