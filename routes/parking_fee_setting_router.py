from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from databases.database import SessionLocal

from schemas import parking_fee_setting_schema
from repositories import parking_fee_setting_repo


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


@router.post("/create_parking_fee", response_model=parking_fee_setting_schema.ResultData, status_code=status.HTTP_201_CREATED)
def create_parking_fee(parking_fee: parking_fee_setting_schema.ParkingFeeSettingCreate, db: Session = Depends(get_db)):
    try:
        created_parking_fee = parking_fee_setting_repo.parking_fee_create_repo(parking_fee=parking_fee, db=db)
        return {"status": True, "message": "created", "data": created_parking_fee}
    except HTTPException as e:
        return JSONResponse(content_return_error(e))

