from fastapi import HTTPException, status
from schemas import schema_parking_master
from sqlalchemy.orm import Session
from models import model


def get_all_parking_master_repo(skip: int, take: int, db: Session):
    parking_master = db.query(model.ParkingMaster).order_by(model.ParkingMaster.id).offset(skip).limit(take).all()
    if not parking_master:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No parking master")
    return parking_master


def create_parking_master_repo(parking: schema_parking_master.ParkingMasterCreate, db: Session):
    create_parking_master = model.ParkingMaster(**parking.model_dump())
    db.add(create_parking_master)
    db.commit()
    db.refresh(create_parking_master)
    return create_parking_master

