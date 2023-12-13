from fastapi import HTTPException, status
from schemas import members_schema, cars_schema
from models import model
from sqlalchemy.orm import Session


def create_car_for_member_repo(owner_id: int, car: cars_schema.CarBase, db: Session):
    try:
        db_car = model.Car(**car.model_dump(), owner_car_id=owner_id)
        db.add(db_car)
        db.commit()
        db.refresh(db_car)
        return db_car
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="error")


def get_member_repo(member_id:int, db: Session):
    member = db.query(model.Member).filter_by(id=member_id).first()
    if member is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this member id is not available")
    return member


def add_member_repo(member: members_schema.MemberCreate, db: Session):
    if not db.query(model.MemberType).filter_by(id=member.member_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Member Type ID not found!")

    create_member = model.Member(**member.model_dump())
    db.add(create_member)
    db.commit()
    db.refresh(create_member)
    return create_member

