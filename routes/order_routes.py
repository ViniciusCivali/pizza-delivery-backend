from fastapi import APIRouter, Depends, HTTPException
from rsa import verify
from dependencies import get_session, OrderSchema, ItemSchema, ResponseOrderSchema, verify_token
from sqlalchemy.orm import Session
from app import Order, User, OrderItem
from typinf import List

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


@order_router.get("/list")
async def list_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    if not user.admin:
        HTTPException(status_code=401, detail="Unauthorized")

    orders = session.query(Order).all()

    return {
        "Orders": orders
    }


@order_router.post("/order/add-item/{order_id}")
async def add_order_item(order_id: int, item_schema: ItemSchema, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(
        Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=400, detail="Orer doesn't exist")

    if order.user_id != user.id and not user.admin:
        raise HTTPException(status_code=401, detail="Unauthorized")

    order_item = OrderItem(
        quantity=item_schema.quantity,
        flavor=item_schema.flavor,
        size=item_schema.size,
        unit_price=item_schema.unit_price,
        order=order_id,
    )

    session.add(order_item)
    order.calculate_price()
    session.commit()

    return {
        "message": "Item added successfully",
        "item_id": order_item.id,
        "order_price": order.price,
    }


@order_router.post("/order/remove-item/{order_item_id}")
async def remove_order_itm(order_item_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order_item = session.query(OrderItem).filter(
        OrderItem.id == order_item_id).first()

    if not order_item:
        raise HTTPException(status_code=400, detail="Orer item doesn't exist")

    order = session.query(Order).filter(Order.id == order_item.order).first()

    if order.user_id != user.id and not user.admin:
        raise HTTPException(status_code=401, detail="Unauthorized")

    session.delete(order_item)
    order.calculate_price()
    session.commit()

    return {
        "message": "Item removed successfully",
        "quantity_order_items": len(order.items),
        "order": order,
    }


# Finish order
@order_router.post("/order/delete-order/{order_id}")
async def delete_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    """
    Delete a order from the user
    """
    order = next(
        (order for order in user.orders if order.id == order_id), None)

    if not order:
        raise HTTPException(
            status_code=401, detail="This user don't have this order")

    session.delete(order)

    session.commit()

    return {
        "message": "Order deleted successfully"
    }


@order_router.post("/order/finish-order/{order_id}")
async def finish_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    """
    Finish a order from the user
    """
    order = next(
        (order for order in user.orders if order.id == order_id), None)

    if not order:
        raise HTTPException(
            status_code=401, detail="This user don't have this order")

    order.status = "FINISHED"

    session.commit()

    return {
        "message": f"Order {order.id} finished successfully",
        "order": order
    }


@order_router.get("/order/get-order/{order_id}", response_model=ResponseOrderSchema)
async def get_user_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    """
    Get a specific order from the user
    """
    order = next(
        (order for order in user.orders if order.id == order_id), None)

    if not order:
        raise HTTPException(
            status_code=401, detail="This user don't have this order")

    return order


@order_router.get("/order/get_order_items/{order_id}")
async def get_order_items(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    """
    Get all items of a especific ordem
    """
    order = next(
        (order for order in user.orders if order.id == order_id), None)

    if not order:
        raise HTTPException(
            status_code=401, detail="This user don't have this order")

    return {
        "orders": order.items
    }


@order_router.get("/order/get-user-orders", response_model=List[ResponseOrderSchema])
async def get_user_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    return {
        "orders": user.orders
    }
