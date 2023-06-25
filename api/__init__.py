from fastapi import APIRouter
from api.warehouse import warehouse_router
from api.product import product_router
from api.auth import auth_router


router = APIRouter(
    prefix="/api",
)

router.include_router(warehouse_router)
router.include_router(product_router)
router.include_router(auth_router)
