from pydantic import BaseModel
from typing import Union, Optional
from datetime import datetime


class EstampTypeMasterBase(BaseModel):
    esta_t_name: str
    active_flag: bool


class EstampTypeMasterCreate(EstampTypeMasterBase):
    pass


class EstampTypeMaster(BaseModel):
    esta_t_id: int
    created_at: datetime
    deleted_at: datetime | None
    updated_at: datetime | None


class ResultData(BaseModel):
    status: bool
    message: str
    data: Union[EstampTypeMaster, dict, list, int, str, None]

    