from datetime import datetime
from typing import Union, Annotated
from pydantic import BaseModel


class ParkingFeeSettingBase(BaseModel):
    pf_hour_01: int
    pf_hour_02: int
    pf_hour_03: int
    pf_hour_04: int
    pf_hour_05: int
    pf_hour_06: int
    pf_hour_07: int
    pf_hour_08: int
    pf_hour_09: int
    pf_hour_10: int
    pf_hour_11: int
    pf_hour_12: int
    pf_hour_13: int
    pf_hour_14: int
    pf_hour_15: int
    pf_hour_16: int
    pf_hour_17: int
    pf_hour_18: int
    pf_hour_19: int
    pf_hour_20: int
    pf_hour_21: int
    pf_hour_22: int
    pf_hour_23: int
    pf_hour_24: int
    pf_day: int
    pf_month: int


class ParkingFeeSettingCreate(ParkingFeeSettingBase):
    parking_code: str


class ParkingFeeSetting(ParkingFeeSettingCreate):
    pf_id: int
    created_at: datetime
    deleted_at: datetime | None
    updated_at: datetime | None


class ResultData(BaseModel):
    status: bool
    message: str
    data: Union[ParkingFeeSetting , list[ParkingFeeSetting], int, str, None]

