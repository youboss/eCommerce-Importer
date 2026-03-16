from fastapi import FastAPI, Form, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import os
import logging

from scrapers.factory import ScraperFactory
from database import init_db, SessionLocal
from product_repository import upsert_product, get_all_products
from batch_sync import sync_products_to_salesforce
import sys
import asyncio
from fastapi.concurrency import run_in_threadpool

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="eCommerce Product Importer")


def _run_in_proactor(coro_fn, *args):
    """Run an async function in a dedicated ProactorEventLoop thread on Windows."""
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        loop = asyncio.ProactorEventLoop()
    else:
        loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro_fn(*args))
    finally:
        loop.close()


# Setup templates and static
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize database on startup
init_db()
logger.info("Database initialized.")


class SalesforceProductRequest(BaseModel):
    name: str
    price: str
    url: str
    image_url: str
    source: str
    sku: Optional[str] = None
    brand: Optional[str] = None
    description: Optional[str] = None


class SyncRequest(BaseModel):
    product_ids: List[int]


# ─── Existing Routes (unchanged logic) ───────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/fetch_products", response_class=HTMLResponse)
async def fetch_products(request: Request, url: str = Form(...)):
    try:
        scraper = ScraperFactory.get_scraper(url)
        products = await run_in_threadpool(_run_in_proactor, scraper.get_products, url)

        # Store scraped products in the database
        db = SessionLocal()
        stored_count = 0
        try:
            for product in products:
                product_data = {
                    "product_name": product.get("name", "Unknown"),
                    "product_url": product.get("url"),
                    "product_code": product.get("sku", ""),  # Use SKU/ASIN as product_code
                    "sku": product.get("sku", ""),
                    "price": product.get("price"),
                    "description": product.get("description", ""),
                    "image_url": product.get("image_url"),
                    "source_platform": product.get("source", scraper.platform_name),
                }
                upsert_product(db, product_data)
                stored_count += 1
        finally:
            db.close()

        logger.info(f"Stored {stored_count} products from {scraper.platform_name}")

        # Redirect to the products table view
        return RedirectResponse(url="/products", status_code=303)

    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        return templates.TemplateResponse("index.html", {"request": request, "error": str(e)})


@app.get("/product_details", response_class=HTMLResponse)
async def product_details(request: Request, url: str):
    try:
        scraper = ScraperFactory.get_scraper(url)
        details = await run_in_threadpool(_run_in_proactor, scraper.get_product_details, url)
        return templates.TemplateResponse("product_detail.html", {"request": request, "product": details, "platform": scraper.platform_name})
    except Exception as e:
        return templates.TemplateResponse("products.html", {"request": request, "error": str(e), "products": []})


@app.post("/save_to_salesforce")
async def save_to_salesforce(product: SalesforceProductRequest):
    """
    Handle single product save from the detail page.
    Uses the new upsert logic and updates the local database if a record exists.
    """
    from services.salesforce_service import SalesforceService
    from product_repository import upsert_product, update_sync_status
    from models import SyncStatus
    
    db = SessionLocal()
    try:
        sf_service = SalesforceService()
        # Convert request model to dict for service
        product_data = {
            "product_name": product.name,
            "product_url": product.url,
            "product_code": product.sku, # Using SKU as code
            "sku": product.sku,
            "price": product.price,
            "description": product.description,
            "image_url": product.image_url,
            "source_platform": product.source
        }
        
        # Upsert in Salesforce
        result = sf_service.upsert_to_salesforce(product_data)
        sf_id = result.get("salesforce_id")
        action = result.get("action")
        
        # Also try to update local DB if it exists (using SKU/code)
        local_p = upsert_product(db, product_data)
        status = SyncStatus.SYNCED if action == "created" else SyncStatus.UPDATED
        update_sync_status(db, local_p.id, status, sf_id)
        
        return {"success": True, "salesforce_id": sf_id, "action": action}
    except Exception as e:
        logger.error(f"Single product sync error: {e}")
        return {"success": False, "error": str(e)}
    finally:
        db.close()


# ─── New Routes (Steps 4–6) ──────────────────────────────────────────────────

@app.get("/products", response_class=HTMLResponse)
async def products_page(request: Request):
    """Serve the DataTables-powered products listing page."""
    return templates.TemplateResponse("products_table.html", {"request": request})


@app.get("/api/products")
async def api_get_products():
    """Return all stored products as JSON for DataTables."""
    db = SessionLocal()
    try:
        products = get_all_products(db)
        return JSONResponse(content={"data": products})
    finally:
        db.close()


@app.post("/api/sync-to-salesforce")
async def api_sync_to_salesforce(sync_request: SyncRequest, background_tasks: BackgroundTasks):
    """Accept selected product IDs and start a background batch sync to Salesforce."""
    if not sync_request.product_ids:
        return JSONResponse(content={"detail": "No product IDs provided."}, status_code=400)

    background_tasks.add_task(sync_products_to_salesforce, sync_request.product_ids)
    logger.info(f"Batch sync started for {len(sync_request.product_ids)} product(s)")

    return JSONResponse(content={
        "message": f"Sync started for {len(sync_request.product_ids)} product(s)",
        "product_ids": sync_request.product_ids
    })


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
