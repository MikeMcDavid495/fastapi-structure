from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas import schema_parking_fee_setting
from models import model


def parking_fee_create_repo(parking_fee: schema_parking_fee_setting.ParkingFeeSettingCreate, db: Session):
    parking_code = db.query(model.ParkingMaster.parking_code).filter_by(parking_code=parking_fee.parking_code).scalar()
    if parking_code is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="cannot reference to parking_code from parking_master")

    create_parking_fee = model.ParkingFeeSetting(**parking_fee.model_dump())
    try:
        db.add(create_parking_fee)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    else:
        db.refresh(create_parking_fee)
        return create_parking_fee

