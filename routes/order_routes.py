from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session, OrderSchema, verify_token
from sqlalchemy.orm import Session
from app import Order, User

order_router = APIRouter(
    prefix="/orders", tags=["orders"], dependencies=[Depends(verify_token)])


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
        user_id=order_shcema.user_id
    )
    session.add(new_order)
    session.commit()
    return {"message": f"Order created with successfully. Order ID: {new_order.id}"}


@order_router.post("order/cancel_order/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(
        Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=400, details="Order not found")

    if not user.admin or order.user_id != user.id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    order.status = "CANCELED"
    session.commit()

    return {
        "message": f"Order {order.id} canceled",
        "order": order
    }
