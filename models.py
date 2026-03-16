import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SAEnum
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SyncStatus(str, enum.Enum):
    NEW = "NEW"
    SYNCED = "SYNCED"
    UPDATED = "UPDATED"
    FAILED = "FAILED"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(500), nullable=False)
    product_url = Column(Text, nullable=True)
    product_code = Column(String(255), nullable=True, index=True)
    sku = Column(String(255), nullable=True, index=True)
    price = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    source_platform = Column(String(100), nullable=True)
    salesforce_id = Column(String(255), nullable=True)
    sync_status = Column(SAEnum(SyncStatus), default=SyncStatus.NEW, nullable=False)
    created_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_date = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                          onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "product_name": self.product_name,
            "product_url": self.product_url,
            "product_code": self.product_code,
            "sku": self.sku,
            "price": self.price,
            "description": self.description,
            "image_url": self.image_url,
            "source_platform": self.source_platform,
            "salesforce_id": self.salesforce_id,
            "sync_status": self.sync_status.value if self.sync_status else "NEW",
            "created_date": self.created_date.isoformat() if self.created_date else None,
            "updated_date": self.updated_date.isoformat() if self.updated_date else None,
        }
