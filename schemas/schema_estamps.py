from pydantic import BaseModel
from typing import Union, Optional
from datetime import datetime


class EstampBase(BaseModel):
    uuid: str
    esta_id: int


class EstampCreate(EstampBase):
    pass


class Estamp(EstampBase):
    e_id: int
    created_at: datetime
    deleted_at: datetime | None
    updated_at: datetime | None


class EstampRegister(BaseModel):
    parking_code: str
    qrcode: str


class ResultData(BaseModel):
    status: bool
    message: str
    data: Union[Estamp, dict, list, int, str, None]

