from pydantic import BaseModel
from typing import Union


class ParkingMasterBase(BaseModel):
    parking_name: str
    location: str
    parking_bays: int


class ParkingMasterCreate(ParkingMasterBase):
    parking_code: str


class ParkingMaster(ParkingMasterCreate):
    id: int


class ResultData(BaseModel):
    status: bool
    message: str
    data: Union[ParkingMaster, int, str, None]

