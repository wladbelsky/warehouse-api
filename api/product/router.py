from fastapi import APIRouter, Depends, HTTPException
from database import Database
from sqlalchemy import select
from api.auth.router import check_token
from typing import List
from .schemas import ProductId as ProductIdSchema, Product as ProductSchema
from .models import Product


router = APIRouter(
    prefix="/product",
)


@router.get("/{product_id}", response_model=ProductIdSchema)
async def get_product(product_id: int, token: str = Depends(check_token)):
    db = await Database()
    async with db.get_session() as session:
        product = (await session.execute(
            select(Product).where(Product.id == product_id)
        )).scalar()
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return ProductIdSchema.from_orm(product)
    

@router.get("/", response_model=List[ProductIdSchema])
async def get_products(token: str = Depends(check_token)):
    db = await Database()
    async with db.get_session() as session:
        products = (await session.execute(select(Product))).scalars()
        return [ProductIdSchema.from_orm(product) for product in products]
    

@router.post("/", response_model=ProductIdSchema)
async def create_product(product: ProductSchema, token: str = Depends(check_token)):
    db = await Database()
    async with db.get_session() as session:
        product_model = Product(**product.dict())
        session.add(product_model)
        await session.commit()
        await session.refresh(product_model)
        return ProductIdSchema.from_orm(product_model)
    

@router.put("/{product_id}", response_model=ProductIdSchema)
async def update_product(product_id: int, product: ProductSchema, token: str = Depends(check_token)):
    db = await Database()
    async with db.get_session() as session:
        product_model: Product = (await session.execute(
            select(Product).where(Product.id == product_id)
        )).scalar()
        if product_model is None:
            raise HTTPException(status_code=404, detail="Product not found")
        for key, value in product.dict().items():
            if key != "id":
                setattr(product, key, value)
        session.add(product_model)
        await session.commit()
        return ProductIdSchema.from_orm(product_model)
    
@router.delete("/{product_id}")
async def delete_product(product_id: int, token: str = Depends(check_token)):
    db = await Database()
    async with db.get_session() as session:
        product: Product = (await session.execute(
            select(Product).where(Product.id == product_id)
        )).scalar()
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        await session.delete(product)
        await session.commit()
        return {"message": "Product deleted"}