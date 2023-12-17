from schemas import orders_schema
from sqlalchemy.orm import Session
from models.model import Order


def create_order_repo(order: orders_schema.OrderCreate, db: Session):
    create_order = Order(**order.model_dump())
    db.add(create_order)
    db.commit()
    db.refresh(create_order)
    return create_order

