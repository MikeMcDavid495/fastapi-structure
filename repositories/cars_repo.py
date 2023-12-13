from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas import cars_schema
from models import model

LIMIT_CARS = 2


def create_cars_repo(car: cars_schema.CarCreate, db: Session):
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
    if cars is None:
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
