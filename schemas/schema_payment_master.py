from pydantic import BaseModel
from typing import Union, Optional
from datetime import datetime


class PaymentMasterBase(BaseModel):
    paym_code: str
    paym_name_th: str
    paym_name_en: str


class PaymentMasterCreate(PaymentMasterBase):
    pass


class PaymentMaster(PaymentMasterBase):
    active_flag: bool = True
    created_at: datetime
    deleted_at: datetime | None
    updated_at: datetime | None


class ResultData(BaseModel):
    status: bool
    message: str
    data: Union[PaymentMaster, dict, list, int, str, None]

