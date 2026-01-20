from fastapi import APIRouter

from .product.views import router as products_router
from .user.views import router as user_router
from .auth.views import router as auth_router
from .cart.views import router as cart_router

router = APIRouter()
router.include_router(router=products_router, prefix='/products')
router.include_router(router=user_router, prefix='/users')
router.include_router(router=auth_router, prefix='/auth')
router.include_router(router=cart_router, prefix='/cart')
