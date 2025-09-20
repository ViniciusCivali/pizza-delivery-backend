from fastapi import APIRouter, Depends
from dependencies import get_session, OrderSchema
from sqlalchemy.orm import Session
from app import Order

order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.get("/")
async def home():
    """
    This is the system's default order route. \n
    All order routes require authentication.
    """
    return {"message": "You have accessed the orders route"}


@order_router.post("/order")
async def create_order(order_shcema: OrderSchema, session: Session = Depends(get_session)):
    """
    Create a order
    """
    new_order = Order(
        user=order_shcema.user
    )
    session.add(new_order)
    session.commit()
    return {"message": f"Order created with successfully. Order ID: {new_order.id}"}
