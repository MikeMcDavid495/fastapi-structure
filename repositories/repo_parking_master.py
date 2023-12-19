from schemas import schema_parking_master
from sqlalchemy.orm import Session
from models import model


def create_parking_master_repo(parking: schema_parking_master.ParkingMasterCreate, db: Session):
    create_parking_master = model.ParkingMaster(**parking.model_dump())
    db.add(create_parking_master)
    db.commit()
    db.refresh(create_parking_master)
    return create_parking_master

