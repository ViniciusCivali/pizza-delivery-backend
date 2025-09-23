from sqlalchemy import (Boolean, Column, Float, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.orm import declarative_base, relationship

# Creatting db conection
db = create_engine("sqlite:///database/banco.db", echo=True, future=True)
# Creating base of db
Base = declarative_base()

# Creating db calsses/tables


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    password = Column("password", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(
        self,
        name: str,
        email: str,
        password: str,
        active: bool = True,
        admin: bool = False,
    ):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin


class Order(Base):
    __tablename__ = "orders"

    # ORDER_STATUS = [
    #     ("PENDING", "PENDING"),
    #     ("CANCELED", "CANCELED"),
    #     ("COMPLETED", "COMPLETED"),
    # ]

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    user_id = Column("user_id", ForeignKey("users.id"))
    price = Column("price", Float)
    items = relationship("OrderItem", cascade="all, delete")

    def __init__(self, price: float = 0, status: str = "PENDING", user_id: int | None = None):
        self.price = price
        self.status = status
        self.user_id = user_id

    def calculate_price(self):
        self.price = sum(item.unit_price *
                         item.quantity for item in self.items)


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantity = Column("quantity", Integer)
    flavor = Column("flavor", String)
    size = Column("size", String)
    unit_price = Column("unit_prie", Float)
    order = Column("order", ForeignKey("orders.id"))

    def __init__(
        self, quantity: int, flavor: str, size: str, unit_price: float, order: int
    ):
        self.quantity = quantity
        self.flavor = flavor
        self.size = size
        self.unit_price = unit_price
        self.order = order

        # Execute the creation of db metadata (Effectively create the db)
