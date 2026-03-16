from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Product, SyncStatus
from datetime import datetime, timezone


def upsert_product(db: Session, data: Dict[str, Any]) -> Product:
    """
    Insert a product or update it if one with the same product_code or sku already exists.
    Returns the Product instance.
    """
    product_code = data.get("product_code") or data.get("sku") or ""
    sku = data.get("sku") or ""

    # Check for existing product by product_code or sku
    existing = None
    if product_code or sku:
        filters = []
        if product_code:
            filters.append(Product.product_code == product_code)
        if sku:
            filters.append(Product.sku == sku)
        existing = db.query(Product).filter(or_(*filters)).first()

    if existing:
        # Update existing record
        existing.product_name = data.get("product_name", existing.product_name)
        existing.product_url = data.get("product_url", existing.product_url)
        existing.price = data.get("price", existing.price)
        existing.description = data.get("description", existing.description)
        existing.image_url = data.get("image_url", existing.image_url)
        existing.source_platform = data.get("source_platform", existing.source_platform)
        existing.updated_date = datetime.now(timezone.utc)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new record
        product = Product(
            product_name=data.get("product_name", "Unknown"),
            product_url=data.get("product_url"),
            product_code=product_code,
            sku=sku,
            price=data.get("price"),
            description=data.get("description"),
            image_url=data.get("image_url"),
            source_platform=data.get("source_platform"),
            sync_status=SyncStatus.NEW,
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        return product


def get_all_products(db: Session) -> List[Dict[str, Any]]:
    """Return all products as a list of dicts."""
    products = db.query(Product).order_by(Product.created_date.desc()).all()
    return [p.to_dict() for p in products]


def get_products_by_ids(db: Session, ids: List[int]) -> List[Product]:
    """Return Product objects matching the given IDs."""
    return db.query(Product).filter(Product.id.in_(ids)).all()


def update_sync_status(db: Session, product_id: int, status: SyncStatus,
                       salesforce_id: Optional[str] = None):
    """Update sync_status and optionally salesforce_id for a product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        product.sync_status = status
        if salesforce_id:
            product.salesforce_id = salesforce_id
        product.updated_date = datetime.now(timezone.utc)
        db.commit()
