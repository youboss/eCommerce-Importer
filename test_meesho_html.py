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
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        print("Navigating to Meesho...")
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(4)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(2)
        content = await page.content()
        with open("meesho_debug.html", "w", encoding="utf-8") as f:
            f.write(content)
        await browser.close()
        print("Done. Saved to meesho_debug.html")

if __name__ == "__main__":
    asyncio.run(main())
