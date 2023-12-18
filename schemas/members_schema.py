import datetime

from pydantic import BaseModel, StringConstraints
from typing import Union, Annotated
from numbers import Real

from schemas.cars_schema import CarBase, Car
from schemas.member_type_schema import MemberType
from schemas.parking_master_schema import ParkingMaster


class MemberBase(BaseModel):
    first_name: str
    last_name: str
    id_card: Annotated[str, StringConstraints(min_length=13, max_length=13)]


class MemberUpdate(BaseModel):
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    id_card: Annotated[str, StringConstraints(min_length=13, max_length=13)] = None
    member_id: int = None


class MemberCreate(MemberBase):
    member_id: int
    member_of_parking: str
    expiry_date: datetime.date


class Member(MemberBase):
    id: int
    member_type_id: MemberType
    cars_owned: list[Car]
    parking: ParkingMaster


class UnionCarMember(MemberBase, Car):
    pass


class ResultData(BaseModel):
    status: bool
    message: str
    data: Union[UnionCarMember, Member, Car, int, str, None]

