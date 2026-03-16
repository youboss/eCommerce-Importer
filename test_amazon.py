import asyncio
import sys
from scrapers.amazon_scraper import AmazonScraper

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

async def main():
    url = "https://www.amazon.in/s?i=computers&rh=n%3A1375425031%2Cp_123%3A46655&dc&qid=1773134125&rnid=91049095031&xpid=qVYfQXx_SEjPW&ref=sr_pg_1"
    scraper = AmazonScraper()
    print("Fetching products...")
    products = await scraper.get_products(url)
    print(f"Fetched {len(products)} products")
    for p in products[:3]:
        print(p)

if __name__ == "__main__":
    asyncio.run(main())
