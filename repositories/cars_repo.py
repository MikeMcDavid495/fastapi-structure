from fastapi import HTTPException, status
from sqlalchemy.orm import Session, defer
from schemas import cars_schema, members_schema
from models import model

import json

LIMIT_CARS = 2


def create_cars_repo(car: cars_schema.CarCreate, db: Session):
    car_owner = db.query(model.Member).filter_by(id=car.owner_id).first()
    if car_owner is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This member is not available")

    owned_cars = db.query(model.Car).filter_by(owner_id=car.owner_id).all()
    if len(owned_cars) >= LIMIT_CARS:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This member reached limit car owned")

    create_car = model.Car(**car.model_dump())
    db.add(create_car)  # add เขียว
    db.commit()  # save
    db.refresh(create_car)
    return create_car


def get_all_cars_repo(skip: int, take: int, db: Session):
    cars = db.query(model.Car).order_by(model.Car.id).offset(skip).limit(take).all()
    if not cars:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No car in database")
    return cars


def get_car_by_id_repo(car_id: int, db: Session):
    if (car := db.query(model.Car).filter_by(id=car_id).first()) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return car


def update_car_repo(car: cars_schema.CarCreate, db: Session):
    if (car_update := db.query(model.Car).filter_by(id=car.owner_id).first()) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

    for var, value in vars(car).items():
        setattr(car_update, var, value) if value is not None else None
    db.commit()
    return car_update


def delete_car_repo(car_id: int, db: Session):
    if (delete_car := db.query(model.Car).filter_by(id=car_id).first()) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Car ID not found")

    db.delete(delete_car)
    db.commit()
    return f'Car id: {car_id} has been deleted!'


def get_member_by_license_plate_repo(license_plate: str, db: Session):
    member = db.query(model.Member).join(model.Car).filter(model.Car.license_plate == license_plate).first()
    car = (
        db.query(model.Car)
        .join(model.Member)
        .filter(model.Member.member_of_parking == "BL100" and model.Car.license_plate == license_plate)
        .options(defer(model.Car.owner_id)).first()
    )
    data = (
        db.query(model.Car, model.Member)
        .filter(model.Member.id == 1)
        .first()
    )

    car_model = cars_schema.Car(**data[0].__dict__)
    member_model = members_schema.MemberBase(**data[1].__dict__)
    # data_x = {**data[0].__dict__, **data[1].__dict__}
    # print(car_model)
    # print(member_model)
    # print(data_x)
    # print({**car_model.model_dump(), **member_model.model_dump()})

    gigi_data = {**car_model.model_dump(), **member_model.model_dump()}

    return gigi_data

