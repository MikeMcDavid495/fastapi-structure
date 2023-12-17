from pydantic import BaseModel
from datetime import datetime
from typing import Union
import uuid


class OrderBase(BaseModel):
    pass


class OrderCreate(OrderBase):
    name: str


class Order(BaseModel):
    id: uuid.UUID
    entry_timestamp: datetime
    name: str


class ResultData(BaseModel):
    status: bool
    message: str
    data: Union[Order, int, str, None]
