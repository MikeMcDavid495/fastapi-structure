import datetime

from pydantic import BaseModel, StringConstraints
from typing import Union, Annotated, Optional
from numbers import Real

from schemas.schema_cars import CarBase, Car
from schemas.schema_member_type import MemberType
from schemas.schema_parking_master import ParkingMaster


class MemberBase(BaseModel):
    first_name: str
    last_name: str
    id_card: int


class MemberCreate(MemberBase):
    member_type_id: int
    member_of_parking: str
    expiry_date: datetime.date


class MemberUpdate(BaseModel):
    id: int

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    id_card: Optional[str] = None

    expiry_date: Optional[datetime.date] = None
    member_id: Optional[int] = None
    member_of_parking: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "normal": [
                {
                    "id": 0,
                    "first_name": "string | replace to null if no change",
                    "last_name": "string | replace to null if no change",
                    "id_card": "string | replace to null if no change",

                    "expiry_date": "date | replace to null if no change",
                    "member_id": "int | replace to null if no change",
                    "member_of_parking": "string | replace to null if no change",
                },
            ]
        }
    }


class Member(MemberBase):
    id: int
    expiry_date: datetime.date


class MemberAll(Member):
    r_member_type_id: MemberType
    cars_owned: list[Car]
    parking: ParkingMaster


class UnionCarMember(MemberBase, Car):
    pass


class ResultData(BaseModel):
    status: bool
    message: str
    data: Union[UnionCarMember, Member, list[MemberAll], Car, int, str, None]

