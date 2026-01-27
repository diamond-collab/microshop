from fastapi import APIRouter

from .product.views import router as product_router
from .order.views import router as order_router
from .user.views import router as user_router


router = APIRouter()

router.include_router(router=product_router)
router.include_router(router=order_router)
router.include_router(router=user_router)
