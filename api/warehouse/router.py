from fastapi import APIRouter, Depends, HTTPException
from database import Database
from sqlalchemy import select
from api.auth.router import check_token
from typing import List
from .models import Warehouse
from .schemas import WarehouseId as WarehouseIdSchema, Warehouse as WarehouseSchema


router = APIRouter(
    prefix="/warehouse",
)


@router.get("/{warehouse_id}", response_model=WarehouseIdSchema)
async def get_warehouse(warehouse_id: int, token: str = Depends(check_token)):
    db = await Database()
    async with db.get_session() as session:
        warehouse = (await session.execute(
            select(Warehouse).where(Warehouse.id == warehouse_id)
        )).scalar()
        if warehouse is None:
            raise HTTPException(status_code=404, detail="Warehouse not found")
        return WarehouseIdSchema.from_orm(warehouse)


@router.get("/", response_model=List[WarehouseIdSchema])
async def get_warehouses(token: str = Depends(check_token)):
    db = await Database()
    async with db.get_session() as session:
        warehouses = (await session.execute(select(Warehouse))).scalars()
        return [WarehouseIdSchema.from_orm(warehouse) for warehouse in warehouses]
    

@router.post("/", response_model=WarehouseIdSchema)
async def create_warehouse(warehouse: WarehouseSchema, token: str = Depends(check_token)):
    db = await Database()
    async with db.get_session() as session:
        warehouse_model = Warehouse(**warehouse.dict())
        session.add(warehouse_model)
        await session.commit()
        await session.refresh(warehouse_model)
        return WarehouseIdSchema.from_orm(warehouse_model)
    

@router.put("/{warehouse_id}", response_model=WarehouseIdSchema)
async def update_warehouse(warehouse_id: int, warehouse: WarehouseSchema, token: str = Depends(check_token)):
    db = await Database()
    async with db.get_session() as session:
        warehouse_model = (await session.execute(
            select(Warehouse).where(Warehouse.id == warehouse_id)
        )).scalar()
        if warehouse_model is None:
            raise HTTPException(status_code=404, detail="Warehouse not found")
        for key, value in warehouse.dict().items():
            if key != "id":
                setattr(warehouse_model, key, value)
        session.add(warehouse_model)
        await session.commit()
        return WarehouseIdSchema.from_orm(warehouse_model)
    

@router.delete("/{warehouse_id}")
async def delete_warehouse(warehouse_id: int, token: str = Depends(check_token)):
    db = await Database()
    async with db.get_session() as session:
        warehouse: Warehouse = (await session.execute(
            select(Warehouse).where(Warehouse.id == warehouse_id)
        )).scalar()
        if warehouse is None:
            raise HTTPException(status_code=404, detail="Warehouse not found")
        await session.delete(warehouse)
        await session.commit()
        return {"message": "Warehouse deleted successfully"}
