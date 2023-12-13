from pydantic import BaseModel
from typing import Union


class CarBase(BaseModel):
    brand: str
    color: str
    license_plate: str
    province: str


class CarCreate(CarBase):
    owner_id: int


class Car(CarBase):
    id: int


class ResultData(BaseModel):
    status: bool
    message: str
    data: Union[Car, list[Car], int, str, None]

