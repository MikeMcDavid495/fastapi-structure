from sqlalchemy.orm import Session
from schemas import schema_parking_fee_setting
from models import model


def parking_fee_create_repo(parking_fee: schema_parking_fee_setting.ParkingFeeSettingCreate, db: Session):
    create_parking_fee = model.ParkingFeeSetting(**parking_fee.model_dump())
    db.add(create_parking_fee)
    db.commit()
    db.refresh(create_parking_fee)
    return create_parking_fee

