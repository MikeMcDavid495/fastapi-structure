from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas import cars_schema
from models import model


def create_cars_repo(car: cars_schema.CarBase, db: Session):
    create_car = model.Car(**car.model_dump())
    db.add(create_car)  # add เขียว
    db.commit()  # save
    db.refresh(create_car)
    return create_car


def get_all_cars_repo(skip: int, take: int, db: Session):
    cars = db.query(model.Car).order_by(model.Car.id).offset(skip).limit(take).all()
    if cars:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No car in database")
    return cars


def get_car_by_id_repo(car_id: int, db: Session):
    car = db.query(model.Car).filter_by(id=car_id).first()
    if car:
        return car
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")


def update_car_repo(car: cars_schema.CarBase, db: Session, car_id: int):
    db.query(model.Car).filter_by(id=car_id).update({**car.model_dump()})
    db.commit()
    return car


def delete_car_repo(car_id: int, db: Session):
    db.query(model.Car).filter_by(id=car_id).delete()
    db.commit()
    return car_id

