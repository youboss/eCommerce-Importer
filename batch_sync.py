import logging
from typing import List
from database import SessionLocal
from product_repository import get_products_by_ids, update_sync_status
from models import SyncStatus
from services.salesforce_service import SalesforceService

logger = logging.getLogger(__name__)


def sync_products_to_salesforce(product_ids: List[int]):
    """
    Background task: batch-sync selected products to Salesforce.
    Authenticates once, then processes each product.
    Updates local DB with salesforce_id and sync_status after each product.
    """
    db = SessionLocal()
    try:
        products = get_products_by_ids(db, product_ids)
        if not products:
            logger.warning("No products found for the given IDs.")
            return

        # Authenticate once for the entire batch
        sf_service = SalesforceService()
        try:
            sf_service.authenticate()
        except Exception as auth_err:
            logger.error(f"Salesforce authentication failed: {auth_err}")
            # Mark all as FAILED
            for product in products:
                update_sync_status(db, product.id, SyncStatus.FAILED)
            return

        # Process each product
        for product in products:
            try:
                product_data = product.to_dict()
                result = sf_service.upsert_to_salesforce(product_data)

                sf_id = result.get("salesforce_id")
                action = result.get("action")

                if action == "created":
                    update_sync_status(db, product.id, SyncStatus.SYNCED, sf_id)
                elif action == "updated":
                    update_sync_status(db, product.id, SyncStatus.UPDATED, sf_id)

                logger.info(f"Product '{product.product_name}' {action} in Salesforce (ID: {sf_id})")

            except Exception as e:
                logger.error(f"Failed to sync product '{product.product_name}': {e}")
                update_sync_status(db, product.id, SyncStatus.FAILED)

    except Exception as e:
        logger.error(f"Batch sync error: {e}")
    finally:
        db.close()
