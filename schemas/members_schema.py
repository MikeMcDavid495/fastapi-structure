from pydantic import BaseModel
from typing import Union

from schemas.cars_schema import CarBase, Car
from schemas.member_type_schema import MemberType


class MemberBase(BaseModel):
    first_name: str
    last_name: str
    id_card: str


class MemberCreate(MemberBase):
    member_id: int


class Member(MemberBase):
    id: int
    member_type_id: MemberType
    cars_owned: list[Car]


class ResultData(BaseModel):
    status: bool
    message: str
    data: Union[Member, int, str, None]