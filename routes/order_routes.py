from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.get("/")
async def orders():
    """
    This is the system's default order route. \n
    All order routes require authentication.
    """

    return {"message": "You have accessed the orders route"}
