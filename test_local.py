import asyncio
import httpx

async def main():
    url = "http://localhost:8000/fetch_products"
    data = {
        "url": "https://www.amazon.in/s?i=computers&rh=n%3A1375425031%2Cp_123%3A46655&dc&qid=1773134125&rnid=91049095031&xpid=qVYfQXx_SEjPW&ref=sr_pg_1"
    }
    
    async with httpx.AsyncClient() as client:
        print("Sending request to local server...")
        resp = await client.post(url, data=data, timeout=120)
        print(f"Status Code: {resp.status_code}")
        if "No products found" in resp.text:
            print("Failed: 'No products found' in HTML.")
        elif "products" in resp.text.lower() and resp.status_code == 200:
            print("Success: Page returned some products!")
            print(f"Length of response: {len(resp.text)} bytes")
        else:
            print("Unknown response:")
            print(resp.text[:500])

if __name__ == "__main__":
    asyncio.run(main())
