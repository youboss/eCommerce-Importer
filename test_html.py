import asyncio
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

async def main():
    url = "https://www.amazon.in/s?i=computers&rh=n%3A1375425031%2Cp_123%3A46655&dc&qid=1773134125&rnid=91049095031&xpid=qVYfQXx_SEjPW&ref=sr_pg_1"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        print("Navigating...")
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(4)
        content = await page.content()
        with open("amazon_debug.html", "w", encoding="utf-8") as f:
            f.write(content)
        await browser.close()
        print("Done. Saved to amazon_debug.html")

if __name__ == "__main__":
    asyncio.run(main())
