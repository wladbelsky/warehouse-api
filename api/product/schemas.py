from pydantic import BaseModel


class Product(BaseModel):
    class Config:
        orm_mode = True
    name: str
    description: str
    price: float
    quantity: int
    warehouse_id: int


class ProductId(Product):
    id: int
