# routes/__init__.py
from .auth_routes import auth_router
from .order_routes import order_router

__all__ = ["auth_router", "order_router"]
