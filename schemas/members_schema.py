from pydantic import BaseModel, StringConstraints
from typing import Union, Annotated
from numbers import Real

from schemas.cars_schema import CarBase, Car
from schemas.member_type_schema import MemberType


class MemberBase(BaseModel):
    first_name: str
    last_name: str
    id_card: Annotated[str, StringConstraints(min_length=13, max_length=13)]


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