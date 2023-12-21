from pydantic import BaseModel
from datetime import datetime
from typing import Union


class EstampMasterBase(BaseModel):
    esta_code: str
    esta_name_th: str
    esta_name_en: str
    active_flag: bool


class EstampMasterCreate(EstampMasterBase):
    esta_t_id: int


class EstampMaster(EstampMasterCreate):
    esta_id: int
    created_at: datetime
    deleted_at: datetime | None
    updated_at: datetime | None


class ResultData(BaseModel):
    status: bool
    message: str
    data: Union[EstampMaster, dict, int, str, list, None]
