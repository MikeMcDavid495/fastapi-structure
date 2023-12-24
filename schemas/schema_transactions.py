from pydantic import BaseModel
from typing import Union, Optional
from datetime import datetime


class TransactionBase(BaseModel):
    t_paid_amount: float
    uuid: str
    paym_id: int


class TransactionCreate(TransactionBase):
    pass


class Transaction(BaseModel):
    t_id: int
    t_paid_datetime: datetime
    created_at: datetime
    deleted_at: datetime | None
    updated_at: datetime | None


class ResultData(BaseModel):
    status: bool
    message: str
    data: Union[Transaction, dict, list, int, str, None]

