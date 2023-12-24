from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from databases.database import SessionLocal

from schemas import schema_parking_fee_setting
from repositories import repo_parking_fee_setting


router = APIRouter(
    prefix="/parking_fee_setting",
    tags=["Parking Fee Setting"],
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


@router.get("/get_all_parking_fee_setting", response_model=schema_parking_fee_setting.ResultData, status_code=status.HTTP_200_OK)
def get_all_parking_fee_setting(skip: int = 0, take: int = 100, db: Session = Depends(get_db)):
    try:
        parking_fee = repo_parking_fee_setting.get_all_parking_fee_setting_repo(skip=skip, take=take, db=db)
        return {"status": True, "message": "created", "data": parking_fee}
    except HTTPException as e:
        return JSONResponse(content_return_error(e))


@router.post("/create_parking_fee", response_model=schema_parking_fee_setting.ResultData, status_code=status.HTTP_201_CREATED)
def create_parking_fee(parking_fee: schema_parking_fee_setting.ParkingFeeSettingCreate, db: Session = Depends(get_db)):
    try:
        created_parking_fee = repo_parking_fee_setting.parking_fee_create_repo(parking_fee=parking_fee, db=db)
        return {"status": True, "message": "created", "data": created_parking_fee}
    except HTTPException as e:
        return JSONResponse(content_return_error(e))

