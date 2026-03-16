import asyncio
import sys
import os

# Add parent directory to path to import scrapers
sys.path.append(os.getcwd())

from scrapers.flipkart_scraper import FlipkartScraper

async def test_flipkart_fix():
    url = "https://www.flipkart.com/6bo/ai3/~cs-w0m7mkua6b/pr?sid=6bo%2Cai3&collection-tab-name=Lenovo&pageCriteria=default&param=82663&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InRpdGxlIjp7Im11bHRpVmFsdWVkQXR0cmlidXRlIjp7ImtleSI6InRpdGxlIiwiaW5mZXJlbmNlVHlwZSI6IlRJVExFIiwidmFsdWVzIjpbIkxlbm92byJdLCJ2YWx1ZVR5cGUiOiJNVUxUSV9WQUxVRUQifX19fX0%3D"
    
    scraper = FlipkartScraper()
    print(f"Testing fix for Flipkart URL: {url}")
    
    products = await scraper.get_products(url)
    
    print(f"\nExtracted {len(products)} products:")
    for i, p in enumerate(products[:5]):
        print(f"{i+1}. Name: {p['name']}")
        print(f"   Price: {p['price']}")
        print(f"   URL: {p['url'][:50]}...")
        print("-" * 20)

if __name__ == "__main__":
    asyncio.run(test_flipkart_fix())
