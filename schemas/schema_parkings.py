from pydantic import BaseModel, Field
from typing import Union, Annotated, Optional
from datetime import datetime
import uuid

from schemas.schema_members import Member


class ParkingBase(BaseModel):
    parking_code: str
    p_license_plate: str
    p_qr_code: Optional[str] = None


class ParkingCreate(ParkingBase):
    uuid: str
    p_time_in: datetime
    p_license_plate_time_in_img_location: str
    p_time_out: Optional[datetime] = None
    p_time_out_expiry_time: Optional[datetime] = None
    p_license_plate_time_out_img_location: str
    p_amount_exc_vat: float
    p_vat: float
    p_amount_inc_vat: float
    p_waived_flag: bool
    member_id: int | None
    member_type_id: int


class ParkingUpdate(BaseModel):
    uuid: str


class Parking(ParkingCreate):
    p_id: int
    created_at: datetime
    deleted_at: datetime | None
    updated_at: datetime | None


class ResultData(BaseModel):
    status: bool
    message: str
    data: Union[Parking, Member, int, str, dict, None]

