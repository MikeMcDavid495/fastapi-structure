from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from dependencies.authen_bearer import JWTBearer
from sqlalchemy.orm import Session
from databases.database import SessionLocal

from schemas import cars_schema
from repositories import cars_repo

router = APIRouter(
    prefix="/cars",
    tags=["cars"],
    dependencies=[Depends(JWTBearer())],
    responses={404: {"data": "not found!"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def content_return_error(e: HTTPException):
    return {"status": False, "message": str(e.detail), "data": None}


# get all
@router.get("/get_all_cars", response_model=cars_schema.ResultData, status_code=status.HTTP_200_OK)
def get_all_cars(skip: int = 0, take: int = 100, db: Session = Depends(get_db)):
    try:
        cars = cars_repo.get_all_cars_repo(skip=skip, take=take, db=db)
        return {"status": True, "message": "get data completed!", "data": cars}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


# get by id
@router.get("/get_car_by_id", response_model=cars_schema.ResultData, status_code=status.HTTP_200_OK)
def get_car_by_id(car_id: int, db: Session = Depends(get_db)):
    try:
        car = cars_repo.get_car_by_id_repo(car_id=car_id, db=db)
        return {"status": True, "message": "get data completed!", "data": car}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


# create
@router.post("/create_car", response_model=cars_schema.ResultData, status_code=status.HTTP_201_CREATED)
def create_car(car: cars_schema.CarBase, db: Session = Depends(get_db)):
    try:
        car_created = cars_repo.create_cars_repo(car=car, db=db)
        if car_created:
            return {"status": True, "message": "created!", "data": car_created}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


# update
@router.put("/update_car", response_model=cars_schema.ResultData, status_code=status.HTTP_200_OK)
def update_car(car: cars_schema.CarBase, car_id: int, db: Session = Depends(get_db)):
    try:
        car_updated = cars_repo.update_car_repo(car=car, db=db, car_id=car_id)
        return {"status": True, "message": "updated!", "data": car_updated}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


# delete
@router.delete("/delete_car", status_code=status.HTTP_202_ACCEPTED)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    try:
        deleted_car = cars_repo.delete_car_repo(car_id=car_id, db=db)
        return {"status": True, "message": "deleted!", "data": deleted_car}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


