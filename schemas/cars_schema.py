from pydantic import BaseModel
from typing import Union


class CarBase(BaseModel):
    brand: str
    color: str
    license_plate: str
    province: str


class ResultData(BaseModel):
    status: bool
    message: str
    data: Union[CarBase, list[CarBase], int, str, None]

