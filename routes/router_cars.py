from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from dependencies.authen_bearer import JWTBearer
from sqlalchemy.orm import Session
from databases.database import SessionLocal

from schemas import schema_cars, schema_members
from repositories import repo_cars

router = APIRouter(
    prefix="/cars",
    tags=["Cars"],
    # dependencies=[Depends(JWTBearer())],
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
@router.get("/get_all_cars", response_model=schema_cars.ResultData, status_code=status.HTTP_200_OK)
def get_all_cars(skip: int = 0, take: int = 100, db: Session = Depends(get_db)):
    try:
        cars = repo_cars.get_all_cars_repo(skip=skip, take=take, db=db)
        return {"status": True, "message": "get data completed!", "data": cars}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


# get by id
@router.get("/get_car_by_id", response_model=schema_cars.ResultData, status_code=status.HTTP_200_OK)
def get_car_by_id(car_id: int, db: Session = Depends(get_db)):
    try:
        car = repo_cars.get_car_by_id_repo(car_id=car_id, db=db)
        return {"status": True, "message": "get data completed!", "data": car}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


# create
@router.post("/create_car", response_model=schema_cars.ResultData, status_code=status.HTTP_201_CREATED)
def create_car(car: schema_cars.CarCreate, db: Session = Depends(get_db)):
    try:
        car_created = repo_cars.create_cars_repo(car=car,  db=db)
        return {"status": True, "message": "created!", "data": car_created}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


# update
@router.put("/update_car", response_model=schema_cars.ResultData, status_code=status.HTTP_200_OK)
def update_car(car: schema_cars.CarCreate, db: Session = Depends(get_db)):
    try:
        car_updated = repo_cars.update_car_repo(car=car, db=db)
        return {"status": True, "message": "updated!", "data": car_updated}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


# delete
@router.delete("/delete_car", status_code=status.HTTP_202_ACCEPTED)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    try:
        deleted_car = repo_cars.delete_car_repo(car_id=car_id, db=db)
        return {"status": True, "message": "deleted!", "data": deleted_car}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


@router.get("/get_member_by_license_plate", response_model=schema_members.ResultData, status_code=status.HTTP_200_OK)
def get_member_by_license_plate(license_plate: str, db: Session = Depends(get_db)):
    try:
        member = repo_cars.get_member_by_license_plate_repo(license_plate=license_plate, db=db)
        return {"status": True, "message": "completed", "data": member}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))

