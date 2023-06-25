from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer, index=True)
    quantity = Column(Integer, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"))
    warehouse = relationship("Warehouse", back_populates="products")