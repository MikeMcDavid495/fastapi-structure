from pydantic import BaseModel
from typing import Union


class MemberTypeBase(BaseModel):
    member_type_name: str


class MemberTypeCreate(MemberTypeBase):
    pass


class MemberType(MemberTypeBase):
    id: int


class ResultData(BaseModel):
    status: bool
    message: str
    data: Union[MemberType, str, int, None]

