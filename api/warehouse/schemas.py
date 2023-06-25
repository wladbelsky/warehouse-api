from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import json


class Warehouse(BaseModel):
    class Config:
        orm_mode = True
    name: str
    address: str
    phone: str
    email: str


class WarehouseId(Warehouse):
    id: int