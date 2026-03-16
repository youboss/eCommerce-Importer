import asyncio
import sys
from playwright.async_api import async_playwright

async def fetch_flipkart():
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    url = "https://www.flipkart.com/6bo/ai3/~cs-w0m7mkua6b/pr?sid=6bo%2Cai3&collection-tab-name=Lenovo&pageCriteria=default&param=82663&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InRpdGxlIjp7Im11bHRpVmFsdWVkQXR0cmlidXRlIjp7ImtleSI6InRpdGxlIiwiaW5mZXJlbmNlVHlwZSI6IlRJVExFIiwidmFsdWVzIjpbIkxlbm92byJdLCJ2YWx1ZVR5cGUiOiJNVUxUSV9WQUxVRUQifX19fX0%3D"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        page = await context.new_page()
        print(f"Navigating to {url}...")
        try:
            # Using wait_until='load' and a long timeout
            await page.goto(url, wait_until='load', timeout=90000)
            print("Page loaded. Waiting for content...")
            await asyncio.sleep(10) # Give more time for JS to render
            
            content = await page.content()
            with open("flipkart_debug_new.html", "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Successfully saved {len(content)} bytes to flipkart_debug_new.html")
            
            await page.screenshot(path="flipkart_debug_new.png")
            print("Screenshot saved to flipkart_debug_new.png")
            
        except Exception as e:
            print(f"Error during navigation: {e}")
            # Try to grab whatever is there
            try:
                content = await page.content()
                with open("flipkart_debug_error.html", "w", encoding="utf-8") as f:
                    f.write(content)
                print("Saved partial content to flipkart_debug_error.html")
            except:
                pass
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(fetch_flipkart())
