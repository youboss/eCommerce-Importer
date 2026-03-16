import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        print("Testing Flipkart...")
        resp = await client.post("http://localhost:8000/fetch_products", data={"url": "https://www.flipkart.com/search?q=laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_4_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_4_na_na_na&as-pos=2&as-type=HISTORY&suggestionId=laptop%7CLaptops&requestId=2bcd2f95-9bdc-4"}, timeout=120)
        print("Flipkart count > 0?:", "items" in resp.text and "No products found" not in resp.text)
        
        print("Testing Meesho...")
        resp = await client.post("http://localhost:8000/fetch_products", data={"url": "https://www.meesho.com/boys-clothes/pl/1nbz"}, timeout=120)
        print("Meesho count > 0?:", "items" in resp.text and "No products found" not in resp.text)

if __name__ == "__main__":
    asyncio.run(main())
