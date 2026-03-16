import asyncio
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

async def main():
    url = "https://www.meesho.com/boys-clothes/pl/1nbz"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()
        print("Navigating to Meesho...")
        await page.goto(url, wait_until="networkidle", timeout=45000)
        await asyncio.sleep(5)
        # scroll down to trigger lazy load
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(3)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(2)
        content = await page.content()
        with open("meesho_debug2.html", "w", encoding="utf-8") as f:
            f.write(content)
        
        # also check for product cards via playwright directly
        cards = await page.query_selector_all('a[href*="/p/"]')
        print(f"Playwright found {len(cards)} links with /p/ in href")
        for card in cards[:3]:
            href = await card.get_attribute('href')
            text = (await card.inner_text())[:100]
            print(f"  href={href!r} text={repr(text)}")
            
        await browser.close()
        print("Done. Saved to meesho_debug2.html")

if __name__ == "__main__":
    asyncio.run(main())
